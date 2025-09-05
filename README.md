# Found Audio Toolkit - Arcade.dev Example

> An example [Arcade.dev](https://arcade.dev) toolkit demonstrating professional software development practices with a simple audio database API.

[![Tests](https://github.com/username/foundaudio-toolkit/workflows/tests/badge.svg)](https://github.com/username/foundaudio-toolkit/actions)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Arcade.dev](https://img.shields.io/badge/Arcade.dev-toolkit-green.svg)](https://arcade.dev)

## 🎯 Project Goals

This project demonstrates how I approach software development by building a **production-ready toolkit** with professional standards:

1. **🏗️ Foundation First**: Establish solid development practices before adding complex features
2. **🧪 Test-Driven**: Comprehensive test coverage with proper mocking and validation
3. **🔧 Tooling**: Modern Python tooling (uv, pytest, linting, CI/CD)
4. **📚 Documentation**: Clear, comprehensive documentation with examples
5. **🚀 Deployment**: Ready for production with proper secret management

The **Found Audio API** was chosen specifically for its simplicity - allowing focus on development practices rather than complex business logic.

## 🛠️ Technology Stack

### Core Framework
- **[Arcade.dev](https://arcade.dev)** - AI tool orchestration platform
- **[Arcade TDK](https://docs.arcade.dev/home/build-tools/create-a-toolkit)** - Toolkit Development Kit

### Python Ecosystem
- **[uv](https://docs.astral.sh/uv/)** - Modern Python package manager
- **[pytest](https://pytest.org)** - Testing framework with async support
- **[Supabase Python](https://supabase.com/docs/reference/python)** - Database client

### Development Tools
- **Pre-commit hooks** - Code quality enforcement
- **GitHub Actions** - Continuous integration
- **Type hints** - Static type checking support

## 🏗️ Architecture

```
foundaudio/
├── foundaudio/           # Main toolkit package
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

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=foundaudio

# Run specific test file
uv run pytest tests/test_get_audio_list.py -v
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

**Returns:** JSON string with audio file metadata including:
- ID, title, description
- File path, duration, genres
- User information and timestamps

### 2. Hello Tool (`say_hello`)

Simple example tool demonstrating basic Arcade functionality.

## 🔐 Secret Management

This toolkit demonstrates [Arcade's secret management](https://docs.arcade.dev/home/build-tools/create-a-tool-with-secrets) system:

```python
@tool(requires_secrets=["SUPABASE_ANON_KEY"])
def get_audio_list(context: ToolContext, ...):
    supabase_key = context.get_secret("SUPABASE_ANON_KEY")
```

**Note:** The Supabase anonymous key is actually public (designed for browser use), but this demonstrates proper secret handling patterns for truly sensitive credentials.

### Setting Up Secrets

1. Go to **Auth > Secrets** in your [Arcade Dashboard](https://dashboard.arcade.dev)
2. Click **"+ Add Secret"**
3. Enter:
   - **ID**: `SUPABASE_ANON_KEY`
   - **Secret Value**: Your Supabase anonymous key
   - **Description**: "Supabase anonymous key for Found Audio database"

## 🧪 Testing Strategy

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

### Running Specific Test Suites

```bash
# Test specific functionality
uv run pytest tests/test_get_audio_list.py::test_get_audio_list_basic -v

# Test with verbose output
uv run pytest -v

# Test with coverage report
uv run pytest --cov=foundaudio --cov-report=html
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
uv run pytest

# Start development server
uv run arcade serve --reload
```

### 2. Code Quality
```bash
# Run pre-commit hooks
pre-commit run --all-files

# Manual linting (if needed)
uv run ruff check foundaudio/
uv run ruff format foundaudio/
```

### 3. Testing Locally
```bash
# Test like CI
./scripts/test-ci-locally.sh
```

## 📚 Learning Resources

### Arcade.dev Documentation
- **[Getting Started](https://docs.arcade.dev/home/quickstart)** - Arcade basics
- **[Building Tools](https://docs.arcade.dev/home/build-tools/create-a-toolkit)** - Tool development
- **[Secret Management](https://docs.arcade.dev/home/build-tools/create-a-tool-with-secrets)** - Handling credentials
- **[Testing Tools](https://docs.arcade.dev/home/evaluate-tools/why-evaluate-tools)** - Evaluation strategies
- **[Deployment](https://docs.arcade.dev/home/serve-tools/arcade-deploy)** - Production deployment

### Python Ecosystem
- **[uv Documentation](https://docs.astral.sh/uv/)** - Modern Python packaging
- **[pytest Documentation](https://docs.pytest.org/)** - Testing framework
- **[Supabase Python Client](https://supabase.com/docs/reference/python)** - Database integration

## 🚀 Production Deployment

### Using Arcade Deploy
```bash
# Deploy to Arcade's managed infrastructure
uv run arcade deploy

# Monitor deployment
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
- Clear documentation and examples

### 3. **Python Ecosystem Mastery**
- Modern tooling (uv instead of pip/poetry)
- Proper package structure and imports
- Type hints and async support
- Testing patterns and mocking

### 4. **Production Readiness**
- CI/CD pipeline with GitHub Actions
- Multiple deployment options
- Monitoring and evaluation capabilities
- Scalable architecture patterns

## 🏆 Key Achievements

✅ **Modern Python Setup** - Using latest tooling and best practices  
✅ **Comprehensive Testing** - Unit, integration, and validation tests  
✅ **Professional CI/CD** - Automated testing and deployment  
✅ **Security Best Practices** - Proper secret management  
✅ **Production Ready** - Multiple deployment options  
✅ **Well Documented** - Clear examples and comprehensive docs  
✅ **Type Safety** - Full type hint coverage  
✅ **Error Handling** - Robust validation and error management  

## 📈 Next Steps

With the solid foundation established, future enhancements could include:

- **Advanced Search** - Fuzzy matching, semantic search
- **Caching Layer** - Redis integration for performance
- **Rate Limiting** - API quota management
- **Monitoring** - Metrics and observability
- **Multi-tenancy** - User-specific data isolation
- **Real-time Features** - WebSocket support for live updates

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Questions?

For questions about this toolkit or Arcade.dev development:

- **Arcade Community**: [Discord](https://discord.gg/arcade)
- **Documentation**: [docs.arcade.dev](https://docs.arcade.dev)
- **Issues**: Create an issue in this repository

---

*Built with ❤️ using [Arcade.dev](https://arcade.dev) - Making AI take action*
