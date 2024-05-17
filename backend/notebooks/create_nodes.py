import pandas as pd
from llama_index.readers.file import MarkdownReader
from pathlib import Path

from markdown_element import MarkdownElementNodeParser
import asyncio
import nest_asyncio
import uvloop

import os
import pickle

if not isinstance(asyncio.get_event_loop(), uvloop.Loop):
    nest_asyncio.apply()

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


reader = MarkdownReader()
charte = reader.load_data(Path("./backend/notebooks/docs/CHARTE_QUALITE_PRODUIT2_Processed.md"))
node_parser = MarkdownElementNodeParser()

if not os.path.exists("./backend/notebooks/docs/charte.pkl"):
    raw_nodes_charte = node_parser.get_nodes_from_documents(charte, show_progress= True)
    pickle.dump(raw_nodes_charte, open("./backend/notebooks/docs/charte.pkl", "wb"))
else:
    raw_nodes_charte = pickle.load(open("./backend/notebooks/docs/charte.pkl", "rb"))



