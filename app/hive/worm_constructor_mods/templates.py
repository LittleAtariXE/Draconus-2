

SHELLCODE_PAYLOAD_TEMPLATE = """
#!name##{{NAME}}
#!itemType##payload
#!info##{{INFO}}

{{SHELLCODE}}
"""

SHELLCODE_FOOD_TEMPLATE = """
#!name##{{NAME}}
#!itemType##food
#!info##{{INFO}}
#!loadType##clean_text

{{SHELLCODE}}
"""


RAW_PAYLOAD_TEMPLATE = """
#!name##{{NAME}}
#!itemType##payload
#!info##{{INFO}}

{{CODE}}
"""

BIN_PAYLOAD_TEMPLATE = """
#!name##{{NAME}}
#!itemType##payload
#!info##{{INFO}}
#!binType##True
#!binName##{{BIN_NAME}}
"""
