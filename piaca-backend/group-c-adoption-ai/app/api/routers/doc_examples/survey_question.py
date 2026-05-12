from fastapi import Body

CREATE_QUESTION_EXAMPLES = Body(
    openapi_examples={
        "text": {
            "summary": "Text question",
            "value": {"type": "text", "question": "Descreva a rotina do seu pet."},
        },
        "boolean": {
            "summary": "Boolean question",
            "value": {"type": "boolean", "question": "Você tem quintal?"},
        },
        "select": {
            "summary": "Select question",
            "value": {
                "type": "select",
                "question": "Com que frequência o pet é vacinado?",
                "possible_answers": [
                    {"option": "Anualmente"},
                    {"option": "A cada 6 meses"},
                    {"option": "Nunca"},
                ],
            },
        },
        "checkbox": {
            "summary": "Checkbox question",
            "value": {
                "type": "checkbox",
                "question": "Quais animais você já teve?",
                "possible_answers": [
                    {"option": "Cachorro"},
                    {"option": "Gato"},
                    {"option": "Pássaro"},
                ],
            },
        },
    }
)

REORDER_QUESTION_EXAMPLES = Body(
    ...,
    embed=True,
    openapi_examples={
        "move_to_first": {
            "summary": "Move to first position",
            "value": {"new_code": 1},
        },
        "move_to_third": {
            "summary": "Move to third position",
            "value": {"new_code": 3},
        },
    },
)

UPDATE_QUESTION_EXAMPLES = Body(
    openapi_examples={
        "update_text": {
            "summary": "Update question text",
            "value": {"question": "Novo texto da pergunta?"},
        },
        "update_type_to_select": {
            "summary": "Change type to select",
            "value": {
                "type": "select",
                "question": "Qual o porte do seu pet?",
                "possible_answers": [
                    {"option": "Pequeno"},
                    {"option": "Médio"},
                    {"option": "Grande"},
                ],
            },
        },
    }
)
