# MegaParse - Your Mega Parser for every type of documents

<div align="center">
    <img src="https://raw.githubusercontent.com/QuivrHQ/MegaParse/main/logo.png" alt="Quivr-logo" width="30%"  style="border-radius: 50%; padding-bottom: 20px"/>
</div>

MegaParse is a powerful and versatile parser that can handle various types of documents with ease. Whether you're dealing with text, PDFs, Powerpoint presentations, Word documents MegaParse has got you covered. Focus on having no information loss during parsing.

## Key Features 🎯

- **Versatile Parser**: MegaParse is a powerful and versatile parser that can handle various types of documents with ease.
- **No Information Loss**: Focus on having no information loss during parsing.
- **Fast and Efficient**: Designed with speed and efficiency at its core.
- **Wide File Compatibility**: Supports Text, PDF, Powerpoint presentations, Excel, CSV, Word documents.
- **Open Source**: Freedom is beautiful, and so is MegaParse. Open source and free to use.

## Support

- Files: ✅ PDF ✅ Powerpoint ✅ Word
- Content: ✅ Tables ✅ TOC ✅ Headers ✅ Footers ✅ Images

### Example

https://github.com/QuivrHQ/MegaParse/assets/19614572/1b4cdb73-8dc2-44ef-b8b4-a7509bc8d4f3

## Installation

```bash
pip install megaparse
```

## Usage

1. Add your OpenAI API key to the .env file

2. Install poppler on your computer (images and PDFs)

3. Install tesseract on your computer (images and PDFs)

```python
from megaparse import MegaParse

megaparse = MegaParse(file_path="./test.pdf")
document = megaparse.load()
print(document.page_content)
megaparse.save_md(document.page_content, "./test.md")
```

### (Optional) Use LlamaParse for Improved Results

1. Create an account on [Llama Cloud](https://cloud.llamaindex.ai/) and get your API key.

2. Call Megaparse with the `llama_parse_api_key` parameter

```python
from megaparse import MegaParse

megaparse = MegaParse(file_path="./test.pdf", llama_parse_api_key="llx-your_api_key")
document = megaparse.load()
print(document.page_content)
```

## BenchMark

<!---BENCHMARK-->

| Parser                                   | Diff |
| ---------------------------------------- | ---- |
| LMM megaparse                            | 36   |
| Megaparse with LLamaParse and GPTCleaner | 74   |
| Megaparse with LLamaParse                | 97   |
| Unstructured Augmented Parse             | 99   |
| LLama Parse                              | 102  |
| **Megaparse**                            | 105  |

<!---END_BENCHMARK-->

_Lower is better_

## Next Steps

- [ ] Improve Table Parsing
- [ ] Improve Image Parsing and description
- [ ] Add TOC for Docx
- [ ] Add Hyperlinks for Docx
- [ ] Order Headers for Docx to Markdown
- [X] Add Rye package manager



## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=QuivrHQ/MegaParse&type=Date)](https://star-history.com/#QuivrHQ/MegaParse&Date)
