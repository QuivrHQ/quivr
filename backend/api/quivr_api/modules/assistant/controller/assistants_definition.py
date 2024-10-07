from quivr_api.modules.assistant.dto.inputs import InputAssistant
from quivr_api.modules.assistant.dto.outputs import (
    AssistantOutput,
    ConditionalInput,
    InputBoolean,
    InputFile,
    Inputs,
    InputSelectText,
    Pricing,
)


def validate_assistant_input(
    assistant_input: InputAssistant, assistant_output: AssistantOutput
):
    errors = []

    # Validate files
    if assistant_output.inputs.files:
        required_files = [
            file for file in assistant_output.inputs.files if file.required
        ]
        input_files = {
            file_input.key for file_input in (assistant_input.inputs.files or [])
        }
        for req_file in required_files:
            if req_file.key not in input_files:
                errors.append(f"Missing required file input: {req_file.key}")

    # Validate URLs
    if assistant_output.inputs.urls:
        required_urls = [url for url in assistant_output.inputs.urls if url.required]
        input_urls = {
            url_input.key for url_input in (assistant_input.inputs.urls or [])
        }
        for req_url in required_urls:
            if req_url.key not in input_urls:
                errors.append(f"Missing required URL input: {req_url.key}")

    # Validate texts
    if assistant_output.inputs.texts:
        required_texts = [
            text for text in assistant_output.inputs.texts if text.required
        ]
        input_texts = {
            text_input.key for text_input in (assistant_input.inputs.texts or [])
        }
        for req_text in required_texts:
            if req_text.key not in input_texts:
                errors.append(f"Missing required text input: {req_text.key}")
            else:
                # Validate regex if applicable
                req_text_val = next(
                    (t for t in assistant_output.inputs.texts if t.key == req_text.key),
                    None,
                )
                if req_text_val and req_text_val.validation_regex:
                    import re

                    input_value = next(
                        (
                            t.value
                            for t in assistant_input.inputs.texts
                            if t.key == req_text.key
                        ),
                        "",
                    )
                    if not re.match(req_text_val.validation_regex, input_value):
                        errors.append(
                            f"Text input '{req_text.key}' does not match the required format."
                        )

    # Validate booleans
    if assistant_output.inputs.booleans:
        required_booleans = [b for b in assistant_output.inputs.booleans if b.required]
        input_booleans = {
            b_input.key for b_input in (assistant_input.inputs.booleans or [])
        }
        for req_bool in required_booleans:
            if req_bool.key not in input_booleans:
                errors.append(f"Missing required boolean input: {req_bool.key}")

    # Validate numbers
    if assistant_output.inputs.numbers:
        required_numbers = [n for n in assistant_output.inputs.numbers if n.required]
        input_numbers = {
            n_input.key for n_input in (assistant_input.inputs.numbers or [])
        }
        for req_number in required_numbers:
            if req_number.key not in input_numbers:
                errors.append(f"Missing required number input: {req_number.key}")
            else:
                # Validate min and max
                input_value = next(
                    (
                        n.value
                        for n in assistant_input.inputs.numbers
                        if n.key == req_number.key
                    ),
                    None,
                )
                if req_number.min is not None and input_value < req_number.min:
                    errors.append(
                        f"Number input '{req_number.key}' is below minimum value."
                    )
                if req_number.max is not None and input_value > req_number.max:
                    errors.append(
                        f"Number input '{req_number.key}' exceeds maximum value."
                    )

    # Validate select_texts
    if assistant_output.inputs.select_texts:
        required_select_texts = [
            st for st in assistant_output.inputs.select_texts if st.required
        ]
        input_select_texts = {
            st_input.key for st_input in (assistant_input.inputs.select_texts or [])
        }
        for req_select in required_select_texts:
            if req_select.key not in input_select_texts:
                errors.append(f"Missing required select text input: {req_select.key}")
            else:
                input_value = next(
                    (
                        st.value
                        for st in assistant_input.inputs.select_texts
                        if st.key == req_select.key
                    ),
                    None,
                )
                if input_value not in req_select.options:
                    errors.append(f"Invalid option for select text '{req_select.key}'.")

    # Validate select_numbers
    if assistant_output.inputs.select_numbers:
        required_select_numbers = [
            sn for sn in assistant_output.inputs.select_numbers if sn.required
        ]
        input_select_numbers = {
            sn_input.key for sn_input in (assistant_input.inputs.select_numbers or [])
        }
        for req_select in required_select_numbers:
            if req_select.key not in input_select_numbers:
                errors.append(f"Missing required select number input: {req_select.key}")
            else:
                input_value = next(
                    (
                        sn.value
                        for sn in assistant_input.inputs.select_numbers
                        if sn.key == req_select.key
                    ),
                    None,
                )
                if input_value not in req_select.options:
                    errors.append(
                        f"Invalid option for select number '{req_select.key}'."
                    )

    # Validate brain input
    if assistant_output.inputs.brain and assistant_output.inputs.brain.required:
        if not assistant_input.inputs.brain or not assistant_input.inputs.brain.value:
            errors.append("Missing required brain input.")

    if errors:
        return False, errors
    else:
        return True, None


assistant1 = AssistantOutput(
    id=1,
    name="Compliance Check",
    description="Allows analyzing the compliance of the information contained in documents against charter or regulatory requirements.",
    pricing=Pricing(),
    tags=["Disabled"],
    input_description="Input description",
    output_description="Output description",
    inputs=Inputs(
        files=[
            InputFile(key="file_1", description="File description"),
            InputFile(key="file_2", description="File description"),
        ],
    ),
    icon_url="https://example.com/icon.png",
)

assistant2 = AssistantOutput(
    id=2,
    name="Consistency Check",
    description="Ensures that the information in one document is replicated identically in another document.",
    pricing=Pricing(),
    tags=[],
    input_description="Input description",
    output_description="Output description",
    icon_url="https://example.com/icon.png",
    inputs=Inputs(
        files=[
            InputFile(key="Document 1", description="File description"),
            InputFile(key="Document 2", description="File description"),
        ],
        select_texts=[
            InputSelectText(
                key="DocumentsType",
                description="Select Documents Type",
                options=[
                    "Cahier des charges VS Etiquettes",
                    "Fiche Dev VS Cahier des charges",
                ],
            ),
        ],
    ),
)

assistant3 = AssistantOutput(
    id=3,
    name="Difference Detection",
    description="Highlights differences between one document and another after modifications.",
    pricing=Pricing(),
    tags=[],
    input_description="Input description",
    output_description="Output description",
    icon_url="https://example.com/icon.png",
    inputs=Inputs(
        files=[
            InputFile(key="Document 1", description="File description"),
            InputFile(key="Document 2", description="File description"),
        ],
        booleans=[
            InputBoolean(
                key="Hard-to-Read Document?", description="Boolean description"
            ),
        ],
        select_texts=[
            InputSelectText(
                key="DocumentsType",
                description="Select Documents Type",
                options=["Etiquettes", "Cahier des charges"],
            ),
        ],
        conditional_inputs=[
            ConditionalInput(
                key="DocumentsType",
                conditional_key="Hard-to-Read Document?",
                condition="equals",
                value="Etiquettes",
            ),
        ],
    ),
)

assistants = [assistant1, assistant2, assistant3]
