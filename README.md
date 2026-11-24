# Ciel

<p align="center">
  <strong>A local AI assistant built for Linux.</strong>
</p>

Ciel is a local AI assistant built with Python and [llama.cpp](https://github.com/ggml-org/llama.cpp), designed to run privately on your own Linux machine.

Powered by locally running open-weight language models, Ciel aims to become a personal desktop assistant capable of natural conversations, remembering previous interactions, helping with programming, and assisting with Linux system operations.

The project is being developed incrementally, starting with a local conversational AI and gradually expanding its memory and system integration capabilities.

## Current Status

**Ciel is under active development.**

The current implementation includes:

- Local AI inference using Qwen3 4B.
- Interactive terminal-based conversations.
- Customizable personality instructions.
- Short-term conversational context.
- Persistent memory storage using SQLite.
- Conversation archiving using JSONL.
- Full-text conversation search using SQLite FTS5.
- Retrieval of relevant previous conversations.

## Features

### Local AI Inference

Ciel uses [llama.cpp](https://github.com/ggml-org/llama.cpp) to run language models locally.

The current setup uses the Qwen3 4B model in GGUF format with Q4_K_M quantization.

### Conversational Context

Ciel maintains recent conversation history during a running session, allowing it to refer to previous messages.

### Persistent Memory

Ciel uses SQLite to store long-term memories separately from its conversation history.

### Conversation Archiving

Conversations are automatically archived in JSONL format, organized by date.

### Conversation Search

SQLite FTS5 provides full-text search across previous conversations. Relevant messages can be retrieved and included as context in new conversations.

### Customizable Personality

Ciel's personality and communication instructions are loaded from a separate text file, allowing users to customize their assistant.

## Technology Stack

| Technology  | Purpose                       |
| ----------- | ----------------------------- |
| Python      | Application logic             |
| llama.cpp   | Local model inference         |
| Qwen3 4B    | Language model                |
| SQLite      | Persistent memory storage     |
| SQLite FTS5 | Full-text conversation search |
| JSONL       | Conversation archiving        |

## Requirements

### Software

- Linux operating system.
- Python 3.9 or newer.
- [llama.cpp](https://github.com/ggml-org/llama.cpp) with `llama-server` available in your PATH.
- SQLite with FTS5 support.
- Git.

Ciel currently uses Python's standard library, so no additional Python packages are required for the existing implementation.

### Hardware

Hardware requirements depend on the language model and its quantization.

The current Qwen3 4B Q4_K_M configuration is intended to run on consumer hardware, including CPU-only systems.

Performance will vary depending on available RAM, CPU, and model configuration. A dedicated GPU is not required, although suitable GPU acceleration can improve inference performance.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/KIRI303/Ciel.git
cd local-llm-learning
```

### 2. Set up the personality configuration

Create your own personality file using the example template:

```bash
cp ciel/personality.example.txt ciel/personality.txt
```

You can customize `ciel/personality.txt` without modifying the example template.

**Note:** Your personal personality configuration is intentionally excluded from Git.

### 3. Start the local model server

Make sure `llama-server` is installed, then run:

```bash
llama-server \
  --hf-repo Qwen/Qwen3-4B-GGUF:Q4_K_M \
  --ctx-size 4096 \
  --host 127.0.0.1 \
  --port 9931 \
  --reasoning off
```

The model will be downloaded automatically if it is not already cached.

Keep this terminal running while using Ciel.

### 4. Start Ciel

Open another terminal in the project directory and run:

```bash
python ciel/chat.py
```

Ciel should now be ready for conversation.

Type `exit` or `quit` to end the session.

## Data Storage and Privacy

Ciel stores its personal data outside the project directory, under:

```text
~/CielData/
├── backups/
├── conversations/
├── documents/
└── memory/
    └── ciel.db
```

The data includes:

- Long-term memories stored in SQLite.
- Daily conversation archives stored as JSONL files.
- Searchable conversation history.

This separation helps prevent personal data from accidentally being included when publishing or updating the source repository.

**Privacy considerations:**

- Conversation archives are stored as local plaintext files.
- Memory data is stored in a local SQLite database.
- The local model server listens on `127.0.0.1`.
- No cloud AI API is required by the current implementation.

Users are responsible for protecting their local data and backups.

## Project Structure

```text
local-llm-learning/
│
├── ciel/
│   ├── chat.py
│   ├── memory.py
│   └── personality.example.txt
│
├── .gitignore
├── LICENSE
└── README.md
```

## Roadmap

Ciel is a learning-driven project, and its development will happen in stages.

### Completed

- [x] Local language model integration.
- [x] Interactive terminal chat.
- [x] Customizable personality.
- [x] Short-term conversational context.
- [x] SQLite-based long-term memory storage.
- [x] JSONL conversation archives.
- [x] Full-text conversation search.

### Planned

- [ ] Improve memory retrieval and relevance.
- [ ] Better persistent conversational memory.
- [ ] Automated testing.
- [ ] Improved error handling and logging.
- [ ] Voice input and speech responses.
- [ ] Linux desktop integration.
- [ ] Permission-controlled system operations.
- [ ] Desktop notifications and background functionality.
- [ ] More customizable assistant settings.

## Contributing

Ciel is an evolving open-source project.

Suggestions, bug reports, and contributions are welcome. Feel free to open an issue or submit a pull request.

As the project develops, contribution guidelines may be added.

## License

This project is licensed under the [MIT License](LICENSE).

The MIT License applies to Ciel's project code. Third-party models, libraries, and dependencies remain subject to their respective licenses.
