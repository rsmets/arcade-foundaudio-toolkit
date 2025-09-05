# Found Audio Toolkit - Arcade.dev Example

> An example [Arcade.dev](https://arcade.dev) toolkit demonstrating professional software development practices with a simple audio database API.

## 🎯 Project Goals

This project demonstrates how I approach software development by building a [toolkit](https://docs.arcade.dev/home/build-tools/create-a-toolkit) with professional software development standards practices:

1. **🏗️ Foundation First**: Establish solid development practices before adding complex features
2. **🧪 Test-Driven**: Comprehensive test coverage with proper mocking and validation
3. **🔧 Tooling**: Modern Python tooling (uv, pytest, linting, CI/CD)
4. **📚 Documentation**: Comprehensive Readme with verbose inline comments

The **Found Audio API** was chosen specifically for its simplicity - allowing focus on development practices rather than complex business logic.

## 🛠️ Tools

### Core Framework

- **[Arcade.dev](https://arcade.dev)** - AI tool orchestration platform
- **[Arcade TDK](https://docs.arcade.dev/home/build-tools/create-a-toolkit)** - Toolkit Development Kit

### Python Ecosystem

- **[uv](https://docs.astral.sh/uv/)** - Modern Python package manager
- **[pytest](https://pytest.org)** - Testing framework with async support
- **[Supabase Python](https://supabase.com/docs/reference/python)** - Database client

### Development Tools

- **Trunk** - [Metalinting](https://docs.trunk.io/code-quality/overview) configuration to enforce standards and best practices
- **GitHub Actions** - Continuous integration
- **Zed** and **Cursor** text editors were used to assist in authoring this toolkit

## 🏗️ File System Layout

```text
foundaudio/
├── foundaudio/          # Main toolkit package
│   ├── __init__.py      # Package initialization
│   └── tools/           # Arcade tools
│       ├── __init__.py  # Tool registration
│       ├── hello.py     # Example tool
│       └── get_audio_list.py  # Main audio search tool
├── tests/               # Test suite
│   ├── test_foundaudio.py
│   └── test_get_audio_list.py
├── evals/               # Evaluation suite
│   └── eval_foundaudio.py
└── scripts/             # Development scripts
    └── test-ci-locally.sh
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd arcadeInterview/foundaudio

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### Starting the Development Server

```bash
# Start Arcade server with auto-reload
uv run arcade serve --reload

# Server will be available at http://localhost:8002
```

## 🔧 Tools Available

### 1. Get Audio List (`get_audio_list`)

Searches the Found Audio database with filtering and pagination.

**Parameters:**

- `limit` (int, optional): Number of results (1-100, default: 20)
- `search` (str, optional): Search term for title/description
- `genre` (str, optional): Filter by genre

**Example Usage:**

```python
# Basic search
result = get_audio_list(limit=5)

# Search with filters
result = get_audio_list(search="pool", genre="House", limit=10)
```

**Returns:** List of audio file dictionaries with metadata including:

- ID, title, description
- File path, duration, genres
- User information and timestamps

## 🔐 Secret Management

This toolkit demonstrates [Arcade's secret management](https://docs.arcade.dev/home/build-tools/create-a-tool-with-secrets) system via [ToolContext](https://docs.arcade.dev/home/build-tools/tool-context). _Please reference the Arcade.dev documentation for information on how to set the Tool secrets_:

```python
@tool(requires_secrets=["SUPABASE_ANON_KEY"])
def get_audio_list(context: ToolContext, ...):
    supabase_key = context.get_secret("SUPABASE_ANON_KEY")
```

**Note:** The Supabase anonymous key is actually public (designed for browser use), but this demonstrates proper secret handling patterns for truly sensitive credentials.

## 🧪 Testing Strategy

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
uv run pytest --cov=foundaudio

# Run specific test file
uv run pytest tests/test_get_audio_list.py -v

# Test specific functionality
uv run pytest tests/test_get_audio_list.py::test_get_audio_list_basic -v
```

### Test Categories

1. **Unit Tests** - Individual function testing with mocking
2. **Integration Tests** - Real API interaction tests
3. **Validation Tests** - Input parameter validation
4. **Error Handling** - Exception and error case testing

### Key Testing Patterns

```python
# Mocking external dependencies
with patch('foundaudio.tools.get_audio_list.create_client') as mock_client:
    mock_context = Mock(spec=ToolContext)
    mock_context.get_secret.return_value = 'test-key'

    result = get_audio_list(mock_context, limit=5)
    assert isinstance(result, str)
```

## 📊 Evaluation

The toolkit includes an evaluation suite for testing tool performance:

```bash
# Run evaluations
uv run python evals/eval_foundaudio.py
```

This demonstrates how to build comprehensive tool evaluation systems for production AI applications.

## 🔄 Development Workflow

### 1. Local Development

```bash
# Install dependencies
uv sync

# Run tests
make test

# Start development server
uv run arcade serve --reload
```

### 2. Code Quality

```bash
# Manual linting; However, this happens as trigger via the Trunk actions
trunk check
trunk fmt
```

### 3. Testing Locally

```bash
# Test like CI
./scripts/test-ci-locally.sh
```

## 📚 Additional Resources

### Arcade.dev Documentation

- **[Getting Started](https://docs.arcade.dev/home/quickstart)** - Arcade basics
- **[Building Tools](https://docs.arcade.dev/home/build-tools/create-a-toolkit)** - Tool development
- **[Secret Management](https://docs.arcade.dev/home/build-tools/create-a-tool-with-secrets)** - Handling credentials
- **[Testing Tools](https://docs.arcade.dev/home/evaluate-tools/why-evaluate-tools)** - Evaluation strategies
- **[Deployment](https://docs.arcade.dev/home/serve-tools/arcade-deploy)** - Production deployment

### Python Tools & Libraries

- **[uv Documentation](https://docs.astral.sh/uv/)** - Modern Python packaging
- **[pytest Documentation](https://docs.pytest.org/)** - Testing framework
- **[Supabase Python Client](https://supabase.com/docs/reference/python)** - Database integration

## 🚀 Production Deployment

### Using Arcade Deploy

```bash
# Deploy to Arcade's managed infrastructure
uv run arcade deploy

# Check deployment status
uv run arcade deploy status
```

See [Arcade's deployment documentation](https://docs.arcade.dev/home/serve-tools/arcade-deploy) for comprehensive deployment options including Docker, Modal, and other hosting platforms.

## 🤝 Development Philosophy

This project exemplifies my approach to software development:

### 1. **Foundation First**

- Establish robust development practices early
- Focus on testing, tooling, and documentation
- Build incrementally with solid foundations

### 2. **Professional Standards**

- Comprehensive test coverage
- Proper error handling and validation
- Security best practices (secret management)
- Comprehensive documentation with verbose inline comments

### 3. **Proper Tooling Leveraged**

- Modern tooling (uv instead of pip/poetry)
- Trunk as a metalinter

### 4. **Production Readiness**

- Evaluation capabilities
- CI/CD set with proper gitops practices enforced

## 📈 Next Steps

With the solid foundation established, future enhancements could include:

- **Evals** - Unfortunatley, upon running `arcade eval`, I was consistently met with [errors](https://github.com/rsmets/arcade-foundaudio-toolkit/issues/9). _Note, I left say_hello tool in the project to have a sansity check baseline... even that eval was not functioning._
- **Multi-tenancy** - User-specific data isolation (would require interfacing with an API in an authenticated state, ie with OAuth)
- **Advanced Search** - Fuzzy matching, semantic search
- **Caching Layer** - To prevent having to call external API all the time
- **Rate Limiting** - API quota management
- **Monitoring** - Metrics and observability.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
