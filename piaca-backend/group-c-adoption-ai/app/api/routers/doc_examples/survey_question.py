from fastapi import Body

CREATE_QUESTION_EXAMPLES = Body(
    openapi_examples={
        "text": {
            "summary": "Text question",
            "value": {
                "type": "text",
                "question": "Descreva sua rotina diária e quanto tempo você tem disponível para dedicar a um pet.",
            },
        },
        "boolean": {
            "summary": "Boolean question",
            "value": {
                "type": "boolean",
                "question": "Você mora em casa com quintal?",
            },
        },
        "select": {
            "summary": "Select question",
            "value": {
                "type": "select",
                "question": "Qual é o seu tipo de moradia?",
                "possible_answers": [
                    {"option": "Casa"},
                    {"option": "Apartamento"},
                    {"option": "Chácara ou sítio"},
                ],
            },
        },
        "checkbox": {
            "summary": "Checkbox question",
            "value": {
                "type": "checkbox",
                "question": "Quem mora com você?",
                "possible_answers": [
                    {"option": "Crianças"},
                    {"option": "Idosos"},
                    {"option": "Outros pets"},
                    {"option": "Moro sozinho(a)"},
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
            "value": {
                "question": "Você tem experiência prévia com animais de estimação?",
            },
        },
        "update_type_to_select": {
            "summary": "Change type to select",
            "value": {
                "type": "select",
                "question": "Qual nível de atividade física você consegue oferecer ao pet?",
                "possible_answers": [
                    {"option": "Baixo — passeios curtos ocasionais"},
                    {"option": "Médio — passeios diários"},
                    {"option": "Alto — exercícios intensos frequentes"},
                ],
            },
        },
    }
)
