

SHELLCODE_PAYLOAD_TEMPLATE = """
#!name##{{NAME}}
#!itemType##payload
#!info##{{INFO}}

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
