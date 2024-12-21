from contextlib import suppress
from talon import Context, Module, actions, settings

mod = Module()

ctx = Context()
ctx.matches = r"""
code.language: c
"""

ctx.lists["self.c_pointers"] = {
    "pointer": "*",
    "pointer to": "*",
}

# fixed-width integer types

ctx.lists["self.stdint_signed"] = {
    "signed": "",
    "unsigned": "u",
    "you": "u",
}

ctx.lists["self.c_type_bit_width"] = {
    "eight": "8",
    "sixteen": "16",
    "thirty two": "32",
    "sixty four": "64",
}

# arithmetic types

ctx.lists["user.c_arithmetic_specifiers"] = {
    "short": 'short',
    "long": 'long',
    "signed": 'signed',
    "unsigned": 'unsigned',
    "char": 'char',
    "car": "char",
    "character": 'char',
    "int": "int",
    "integer": "int",
    "double": 'double',
    "float": 'float',
    "void": "void", #todo base types
}

ctx.lists["user.c_qualifiers"] = {
    "static": "static",
    "constant": "const",
    "const": "const",
    "volatile": "volatile",
    "extern": "extern",
}

ctx.lists["user.c_declarators"] = {
    "array": "array",
    "pointer": "pointer",
}

#### OLD

ctx.lists["self.c_signed"] = {
    "signed": "signed ",
    "unsigned": "unsigned ",
}

ctx.lists["self.c_keywords"] = {
    "static": "static",
    "volatile": "volatile",
    "register": "register",
}


ctx.lists["user.code_libraries"] = {
    "assert": "assert.h",
    "type": "ctype.h",
    "error": "errno.h",
    "float": "float.h",
    "limits": "limits.h",
    "locale": "locale.h",
    "math": "math.h",
    "set jump": "setjmp.h",
    "signal": "signal.h",
    "arguments": "stdarg.h",
    "definition": "stddef.h",
    "input": "stdio.h",
    "output": "stdio.h",
    "library": "stdlib.h",
    "string": "string.h",
    "time": "time.h",
    "standard int": "stdint.h",
 
}

ctx.lists["user.c_common_function"] = {
    "mem copy": "memcpy",
    "mem set": "memset",
    "string cat": "strcat",
    "stir cat": "strcat",
    "stir en cat": "strncat",
    "stir elle cat": "strlcat",
    "stir copy": "strcpy",
    "stir en copy": "strncpy",
    "stir elle copy": "strlcpy",
    "string char": "strchr",
    "string dupe": "strdup",
    "stir dupe": "strdup",
    "stir comp": "strcmp",
    "stir en comp": "strncmp",
    "string len": "strlen",
    "stir len": "strlen",
    "is digit": "isdigit",
    "get char": "getchar",
    "print eff": "printf",
    "es print eff": "sprintf",
    "es en print eff": "sprintf",
    "stir to int": "strtoint",
    "stir to unsigned int": "strtouint",
    "ay to eye": "atoi",
    "em map": "mmap",
    "ma map": "mmap",
    "em un map": "munmap",
    "size of": "sizeof",
    "ef open": "fopen",
    "ef write": "fwrite",
    "ef read": "fread",
    "ef close": "fclose",
    "exit": "exit",
    "signal": "signal",
    "set jump": "setjmp",
    "get op": "getopt",
    "malloc": "malloc",
    "see alloc": "calloc",
    "alloc ah": "alloca",
    "re alloc": "realloc",
    "free": "free",
}

ctx.lists["user.code_common_function"] = ctx.lists["user.c_common_function"]

mod.list("c_type_bit_width", desc="Common C type bit widths")
mod.list("c_arithmetic_specifiers", desc="C type specifiers")
mod.list("c_qualifiers", desc="C type qualifiers")
mod.list("c_common_function", desc="common C functions")
mod.list("c_declarators", desc="common C declarators")

mod.list("c_pointers", desc="Common C pointers")
mod.list("c_signed", desc="Common C datatype signed modifiers")
mod.list("c_keywords", desc="C keywords")
mod.list("stdint_signed", desc="Common stdint C datatype signed modifiers")


@mod.capture(rule="{self.c_pointers}")
def c_pointers(m) -> str:
    "Returns a string"
    return m.c_pointers


@mod.capture(rule="{self.c_signed}")
def c_signed(m) -> str:
    "Returns a string"
    return m.c_signed


@mod.capture(rule="{self.c_keywords}")
def c_keywords(m) -> str:
    "Returns a string"
    return m.c_keywords

@mod.capture(rule="{self.stdint_signed}")
def stdint_signed(m) -> str:
    "Returns a string"
    return m.stdint_signed

@mod.capture(rule="{self.c_type_bit_width}")
def c_type_bit_width(m) -> str:
    "Returns a string"
    return m.c_type_bit_width

@mod.capture(rule="{self.c_arithmetic_specifiers}")
def c_arithmetic_specifier(m) -> str:
    "Returns a string"
    return m.c_arithmetic_specifiers

# fixed-width integer types
@mod.capture(rule="[<self.stdint_signed>] int <self.c_type_bit_width>")
def c_fixed_integer(m) -> str:
    "Returns a string"
    prefix = ""
    with suppress(AttributeError):
        prefix = m.stdint_signed
    return prefix + "int" + m.c_type_bit_width + "_t"

# arithmetic types
@mod.capture(rule="<self.c_arithmetic_specifier>+")
def c_arithmetic_type(m) -> str:
    "Returns a string"
    return " ".join(m.c_arithmetic_specifier_list)

@mod.capture(rule="<self.c_fixed_integer>|<self.c_arithmetic_type>")
def c_raw_type(m) -> str:
    "Returns a string"
    return str(m)

@mod.capture(rule="<self.c_raw_type> [<self.c_pointers>+]")
def c_type(m) -> str:
    "Returns a string"
    suffix = ""
    with suppress(AttributeError):
        suffix = "".join(m.c_pointers_list)
    return m.c_raw_type+suffix

@mod.capture(rule="{self.c_declarators}* <user.text>")
def c_variable(m) -> str:
    "Returns a string"
    name = actions.user.formatted_text(
                m.text,
                settings.get("user.code_private_variable_formatter")
            )
    with suppress(AttributeError):
        if 'array' in m.c_declarators_list:
            name = name+"[]"
        if 'pointer' in m.c_declarators_list:
            name = "*"+name
    return name

@mod.capture(rule="{self.c_qualifiers}")
def c_qualifier(m) -> str:
    "Returns a string"
    return m.c_qualifiers

@mod.capture(rule="<self.c_qualifier>+")
def c_qualifier_list(m) -> str:
    "Returns a string"
    return " ".join(m.c_qualifier_list)+" "


@ctx.action_class("user")
class UserActions:
    def code_operator_indirection():
        actions.auto_insert("*")

    def code_operator_address_of():
        actions.auto_insert("&")

    def code_operator_structure_dereference():
        actions.auto_insert("->")

    def code_operator_subscript():
        actions.insert("[]")
        actions.key("left")

    def code_operator_assignment():
        actions.auto_insert(" = ")

    def code_operator_subtraction():
        actions.auto_insert(" - ")

    def code_operator_subtraction_assignment():
        actions.auto_insert(" -= ")

    def code_operator_addition():
        actions.auto_insert(" + ")

    def code_operator_addition_assignment():
        actions.auto_insert(" += ")

    def code_operator_multiplication():
        actions.auto_insert(" * ")

    def code_operator_multiplication_assignment():
        actions.auto_insert(" *= ")

    # action(user.code_operator_exponent): " ** "
    def code_operator_division():
        actions.auto_insert(" / ")

    def code_operator_division_assignment():
        actions.auto_insert(" /= ")

    def code_operator_modulo():
        actions.auto_insert(" % ")

    def code_operator_modulo_assignment():
        actions.auto_insert(" %= ")

    def code_operator_equal():
        actions.auto_insert(" == ")

    def code_operator_not_equal():
        actions.auto_insert(" != ")

    def code_operator_greater_than():
        actions.auto_insert(" > ")

    def code_operator_greater_than_or_equal_to():
        actions.auto_insert(" >= ")

    def code_operator_less_than():
        actions.auto_insert(" < ")

    def code_operator_less_than_or_equal_to():
        actions.auto_insert(" <= ")

    def code_operator_and():
        actions.auto_insert(" && ")

    def code_operator_or():
        actions.auto_insert(" || ")

    def code_operator_bitwise_and():
        actions.auto_insert(" & ")

    def code_operator_bitwise_and_assignment():
        actions.auto_insert(" &= ")

    def code_operator_bitwise_or():
        actions.auto_insert(" | ")

    def code_operator_bitwise_or_assignment():
        actions.auto_insert(" |= ")

    def code_operator_bitwise_exclusive_or():
        actions.auto_insert(" ^ ")

    def code_operator_bitwise_exclusive_or_assignment():
        actions.auto_insert(" ^= ")

    def code_operator_bitwise_left_shift():
        actions.auto_insert(" << ")

    def code_operator_bitwise_left_shift_assignment():
        actions.auto_insert(" <<= ")

    def code_operator_bitwise_right_shift():
        actions.auto_insert(" >> ")

    def code_operator_bitwise_right_shift_assignment():
        actions.auto_insert(" >>= ")

    def code_insert_null():
        actions.auto_insert("NULL")

    def code_insert_is_null():
        actions.auto_insert(" == NULL ")

    def code_insert_is_not_null():
        actions.auto_insert(" != NULL")

    def code_state_if():
        actions.insert("if (")
        #actions.key("left")
        #actions.insert("if () {\n}\n")
        #actions.key("up:2 left:3")

    def code_state_else_if():
        actions.insert("else if (")
        #actions.key("left")
        #actions.insert("else if () {\n}\n")
        #actions.key("up:2 left:3")
        

    def code_state_else():
        actions.insert("else {")
        actions.key("enter")
        # actions.insert("else\n{\n}\n")
        # actions.key("up:2")

    def code_state_switch():
        actions.insert("switch ()")
        actions.edit.left()

    def code_state_case():
        actions.insert("case \nbreak;")
        actions.edit.up()

    def code_state_for():
        actions.auto_insert("for ")

    def code_state_go_to():
        actions.auto_insert("goto ")

    def code_state_while():
        actions.insert("while ()")
        actions.edit.left()

    def code_state_return():
        actions.auto_insert("return ")

    def code_break():
        actions.auto_insert("break;")

    def code_next():
        actions.auto_insert("continue;")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_comment_line_prefix():
        actions.auto_insert("//")

    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + f"({selection})"
        else:
            text = text + "()"

        actions.user.paste(text)
        actions.edit.left()

    # TODO - it would be nice that you integrate that types from c_cast
    # instead of defaulting to void
    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_private_static_function(text: str):
        """Inserts private static function"""
        result = "static void {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.code_insert_function(result, None)

    def code_insert_library(text: str, selection: str):
        actions.user.paste(f"#include <{text}>")

