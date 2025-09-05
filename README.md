# Found Audio Toolkit - Arcade.dev Example

> An example [Arcade.dev](https://arcade.dev) toolkit demonstrating professional software development practices with a simple audio database API as requested in the take-home [assignment](ArcadeEngineeringInterviewProject.pdf). The downstream usage of this toolkit can be found the [arcade-mastra-agent](https://github.com/rsmets/arcade-mastra-agent) repo.

## 🎯 Project Goals

This project demonstrates how I approach software development by building a [toolkit](https://docs.arcade.dev/home/build-tools/create-a-toolkit) with professional software development standards practices:

1. **🏗️ Foundation First**: Establish solid development practices before adding higher-level features/tools.
2. **🧪 Test-Driven**: Comprehensive test coverage with proper mocking and validation
3. **🔧 Tooling**: Modern Python tooling (uv, pytest, metalinting via [Trunk](https://docs.trunk.io/code-quality/overview) (more comprehensive than what the scaffolding provided), tests run via standard trunk-based development gitops workflows via CI/CD)
4. **📚 Documentation**: Comprehensive Readme with verbose inline comments

The [Found Audio](https://foundaudio.club) search API was chosen specifically for its simplicity - allowing focus on development practices rather than complex business logic. _Note: I created and operate Found Audio._

### Concessions

I really wanted to make a complex toolkit that would require OAuth to interface with a popular API that is currently not listed as a public [integration](https://docs.arcade.dev/toolkits), for example Uber's API, but given the time constraint I opted to keep the API integration aspect of this project as simple as possible. Given the fact that this is a professional role's technical assessment, I emphasized spending my time showcasing professional development practices rather than more interesting business logic.

## 🛠️ Tools

### Core Framework

- **[Arcade.dev](https://arcade.dev)** - AI tool orchestration platform
- **[Arcade TDK](https://docs.arcade.dev/home/build-tools/create-a-toolkit)** - Toolkit Development Kit

### Python Ecosystem

- **[uv](https://docs.astral.sh/uv/)** - Modern Python package manager
- **[pytest](https://pytest.org)** - Testing framework with async support
- **[Supabase Python](https://supabase.com/docs/reference/python)** - Database client

### Development Tools

- **[Trunk](https://trunk.io/)** - [Metalinting](https://docs.trunk.io/code-quality/overview) configuration to enforce standards and best practices. It should just work thanks to the [Launcher](https://docs.trunk.io/code-quality/setup-and-installation/initialize-trunk#the-trunk-launcher) however, it might require a separate install (I was not able to verify; I have it globally on my machine)
- **[GitHub Actions](https://docs.github.com/en/actions)** - Continuous integration
- **[Zed](https://zed.dev/)** and **[Cursor](https://cursor.com/agents)** text editors were used with a variety of foundation models to assist in authoring this toolkit

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
git clone https://github.com/rsmets/arcade-foundaudio-toolkit.git
cd arcadeInterview/foundaudio

# Install dependencies
make install

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
```

### Starting the Development Server

```bash
# Start Arcade server with auto-reload
uv run arcade serve --reload

# Server will be available at http://localhost:8002
```

Follow along the Arcade.dev [documentation](https://docs.arcade.dev/home/build-tools/create-a-toolkit#connect-your-toolkit-to-the-arcade-engine) on how to port-forward your local instance for testing the tool calling within the Arcade.dev dashboard.

## 🔧 Tools Available

For the sake of time and simplicity, I opted not to invest effort into more than one tool call.

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

This toolkit demonstrates [Arcade's secret management](https://docs.arcade.dev/home/build-tools/create-a-tool-with-secrets) system via [ToolContext](https://docs.arcade.dev/home/build-tools/tool-context). _Please reference the Arcade.dev documentation for information on how to set the `SUPABASE_ANON_KEY` Tool secret in your dashboard._:

```python
@tool(requires_secrets=["SUPABASE_ANON_KEY"])
def get_audio_list(context: ToolContext, ...):
    supabase_key = context.get_secret("SUPABASE_ANON_KEY")
```

**Note:** The Supabase [anonymous key](https://supabase.com/docs/guides/api/api-keys#anon-and-publishable-keys) is actually public, but this demonstrates proper secret handling patterns for truly sensitive credentials.

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
2. **Validation Tests** - Input parameter validation
3. **Error Handling** - Exception and error case testing
4. **Integration Tests** - Real API interaction tests _TODO: opted to keep the API mocked for simplicity_

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

The toolkit attempted to include an evaluation suite for testing tool performance however as documented in an [issue](https://github.com/rsmets/arcade-foundaudio-toolkit/issues/9), I was unable to even run the scaffolding `say_hello` eval. _Note: I kept the `say_hello` tool defined in this project for a baseline sanity purposes; if this were a published toolkit, that would be the first cleanup item removed._

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
- Trunk as a [metalinting](https://docs.trunk.io/code-quality/overview) configuration to enforce source code standards and best practices.

### 4. **Production Readiness**

- Evaluation capabilities
- CI/CD set with proper gitops practices enforced

## 🏆 Outcome

I feel all of the [project goals](#-project-goals) were achieved. I was able to successfully deploy my worker to Arcade.dev using Cloudflare and test via the dashboard tool calling interface.

Worker URI: `https://e58rbgi8n1svd5mpt8rxtr316-1972021761134002131.server.arcade.dev`
Secret: `<default suggestion>`

_It is unclear to me the best way to provide the information necessary for others to interface with this toolkit... the [deploy documentation](https://docs.arcade.dev/home/serve-tools/arcade-deploy) does not include information on this._

## 📈 Next Steps

With the solid foundation established, future enhancements could include:

- **Evals** - Unfortunately, upon running `arcade eval`, I was consistently met with [errors](https://github.com/rsmets/arcade-foundaudio-toolkit/issues/9). _Note, I left `say_hello` tool in the project to have a sanity check baseline, but even that eval was not functioning._
- **Multi-tenancy** - User-specific data isolation (would require interfacing with an API in an authenticated state, ie with OAuth)
- **More Tools** - Use more of the Found Audio api to do things like get profile/user info.
- **User Auth** - Add tools that require Found Audio user authentication, eg post comments and like audio files.
- **Caching Layer** - To prevent having to call the external API all the time
- **Monitoring** - Metrics and observability.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
