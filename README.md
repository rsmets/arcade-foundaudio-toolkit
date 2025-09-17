# Arcade.dev Found Audio Toolkit

> An example [Arcade.dev](https://arcade.dev) toolkit demonstrating professional software development practices with a simple audio database API as requested in the take-home [assignment](ArcadeEngineeringInterviewProject.pdf). The downstream usage of this toolkit can be found the [arcade-mastra-agent](https://github.com/rsmets/arcade-mastra-agent) repo.

## Project Goals

This project demonstrates how I approach software development by building a [toolkit](https://docs.arcade.dev/home/build-tools/create-a-toolkit) with professional software development standards practices:

1. **Foundation First**: Establish solid development practices before adding higher-level features/tools.
2. **Test-Driven**: Comprehensive test coverage with proper mocking and validation
3. **Tooling**: Metalinting via [Trunk](https://docs.trunk.io/code-quality/overview) (more comprehensive than what the scaffolding provided), tests, evals, and deployments run via standard trunk-based development gitops workflows via CI/CD). Text editor commands and rules to assist with common workflows (Cursor commands and rules).
4. **Documentation**: Comprehensive Readme with verbose inline comments
5. **Production Readiness**: Comprehensive evaluation suites to ensure tool performance and AI assistant behavior. Automated deployment pipelines based on trunk-based GitOps practices.

### Integration

The [Found Audio](https://foundaudio.club) search API was chosen specifically for its simplicity - allowing focus on development practices rather than complex business logic. _Note: I created and operate Found Audio._

#### Concession

I really wanted to make a complex toolkit that would require OAuth to interface with a popular API that is currently not listed as a public [integration](https://docs.arcade.dev/toolkits), for example Uber's API, but given the time constraint I opted to keep the API integration aspect of this project as simple as possible. I emphasized spending my time showcasing professional development practices rather than more interesting business logic.

### Toolkit Design

This toolkit follows MCP design best practices [[1]](https://liquidmetal.ai/casesAndBlogs/mcp-api-wrapper-antipattern/) [[2]](https://vercel.com/blog/the-second-wave-of-mcp-building-for-llms-not-developers), particularly to avoid common API wrapper anti-patterns.

#### Design Principles

1. **Design for Intent, Not API Mapping**
   - Focus on user workflows rather than individual API endpoints
   - Map what users actually want to accomplish with the service
   - Handle complexity internally (name resolution or ambiguity)
   - Example: "Search for audio files by Fidelio" makes multiple API calls but still only uses a single tool. Let the LLM focus on the actual task instead of system integration

2. **Design Responses for Language Models**
   - Return structured, concise information
   - Skip unnecessary data that clutters AI agent context
   - Focus on what the LLM needs to complete the task

3. **Handle Errors Like a Helpful Colleague**
   - Provide clear explanations of what went wrong
   - Suggest specific next steps for recovery
   - Use `RetryableToolError` for user-fixable issues with actionable guidance

#### Implementation in This Toolkit

Our [`get_audio_list`](./foundaudio/foundaudio/tools/get_audio_list.py) tool demonstrates these principles:

- **Single Intent**: One call searches and filters audio files (potentially with multiple API calls within a single tool call)
- **Intelligent Error Handling**: Clear validation messages with specific parameter guidance
- **Structured Responses**: Clean data models that AI agents can easily work with

## Tools

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
- Cursor rules and commands ([released](https://cursor.com/changelog) Sept 11th)
- Arcade documentation MCP server (and vector embeddings) created and hosted with [Ref](https://ref.tools/dashboard)

## File System Layout

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

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/rsmets/arcade-foundaudio-toolkit.git
cd foundaudio

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

## Tools Available

For the sake of time and simplicity, I opted not to invest effort into more than one tool call.

### 1. Get Audio List, [`get_audio_list`](./foundaudio/foundaudio/tools/get_audio_list.py)

Searches the Found Audio database with filtering and pagination.

**Parameters:**

- `limit` (int, optional): Number of results (1-100, default: 20)
- `search` (str, optional): Search term for title/description
- `genre` (str, optional): Filter by genre
- `username` (str, optional): Filter by specific user's audio files

**Example Usage:**

```python
# Basic search
result = get_audio_list(limit=5)

# Search with filters
result = get_audio_list(search="pool", genre="House", limit=10)

# Get audio files from a specific user
result = get_audio_list(username="discodude", limit=10)

# Combine username with other filters
result = get_audio_list(username="discodude", search="house", genre="electronic", limit=5)
```

**Returns:** List of audio file dictionaries with metadata, for example:

```json
{
  "created_at": "2025-08-31T04:16:21.395954+00:00",
  "description": "Please ensure your subs are at the right woof levels. Strap yourself in and lets take some hot laps around some hard tracks 🏎️",
  "duration": 2256.17,
  "genres": ["HEATERS"],
  "id": "f52d92b3-c590-4d80-a64a-89f972bb61c4",
  "title": "Can It Get Much Harder Vol.6",
  "updated_at": "2025-08-31T04:16:21.395954+00:00",
  "url": "https://foundaudio.club/audio/f52d92b3-c590-4d80-a64a-89f972bb61c4",
  "user_id": "1ffbf508-7d8a-43f0-8312-8a3a7176a919"
}
```

## Secret Management

This toolkit demonstrates [Arcade's secret management](https://docs.arcade.dev/home/build-tools/create-a-tool-with-secrets) system via [ToolContext](https://docs.arcade.dev/home/build-tools/tool-context). _Please reference the Arcade.dev documentation on how to set the `SUPABASE_ANON_KEY` Tool secret in your dashboard._:

```python
@tool(requires_secrets=["SUPABASE_ANON_KEY"])
def get_audio_list(context: ToolContext, ...):
    supabase_key = context.get_secret("SUPABASE_ANON_KEY")
```

**Note:** The Supabase [anonymous key](https://supabase.com/docs/guides/api/api-keys#anon-and-publishable-keys) is actually public, but this demonstrates proper secret handling patterns for truly sensitive credentials.

## Testing Strategy

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
4. **Evaluations (~E2E Tests)** - Real API and LLM interaction tests

### Key Testing Patterns

```python
# Mocking external dependencies
with patch('foundaudio.tools.get_audio_list.create_client') as mock_client:
    mock_context = Mock(spec=ToolContext)
    mock_context.get_secret.return_value = 'test-key'

    result = get_audio_list(mock_context, limit=5)
    assert isinstance(result, str)
```

## Evaluation

The toolkit includes comprehensive evaluation suites for testing tool performance and AI assistant behavior. The evaluation suites are located in the `foundaudio/evals/` directory:

- `eval_foundaudio.py` - Audio search tool evaluations
- `eval_hello.py` - Hello tool evaluations

### Evaluation Categories

#### 1. **Hello Tool Evaluations** (`eval_hello.py`)

- Simple greeting scenarios
- Contextual greetings with conversation history
- Name extraction and parameter passing
- Edge cases (empty names, special characters)
- Multi-turn conversation flow

#### 2. **Audio Search Tool Evaluations** (`eval_foundaudio.py`)

- **Basic Functionality**: No filters, limit parameters, search terms, genre filters
- **Combined Filters**: Multiple parameter combinations (limit + search + genre)
- **Parameter Validation**: Boundary testing (min/max limits)
- **Edge Cases**: Empty search terms, whitespace handling, special characters
- **Complex Scenarios**: Multi-genre context, artist-specific searches, duration context
- **Conversation Context**: Multi-turn conversations with user preferences
- **Error Scenarios**: Invalid parameter handling

#### 3. **Critic Types Used**

- `BinaryCritic`: Exact parameter matching
- `SimilarityCritic`: Semantic similarity for search terms and genres
- `NumericCritic`: Numeric parameter validation with tolerance

### Running Evaluations

```bash
# Option 1: Using Makefile (recommended)
make evals

# Option 2: Manual commands
cd foundaudio/evals

# Run all evaluations
arcade evals -h api.arcade.dev .

# Run specific evaluation files
arcade evals -h api.arcade.dev eval_foundaudio.py  # Audio search tool only
arcade evals -h api.arcade.dev eval_hello.py       # Hello tool only
```

### Evaluation Rubric

The evaluation suite uses a rubric with:

- **Fail Threshold**: 0.8 (80% accuracy required)
- **Warn Threshold**: 0.9 (90% accuracy for warnings)

This comprehensive evaluation suite ensures the AI assistant correctly:

- Extracts user intent from natural language
- Applies appropriate filters and parameters
- Handles edge cases and error scenarios
- Maintains context across conversation turns
- Validates input parameters properly

_Note: The `say_hello` tool is included for baseline testing and can be removed in production deployments._

## Development Workflow

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
# Manual linting; However, this happens automatically via git hooks and are run in CI
trunk check
trunk fmt
```

### 3. Testing Locally

```bash
make tests
```

## Production Deployment

### Manual Deployment

```bash
# Deploy to Arcade's managed infrastructure
make deploy
```

### Automated Deployment

The project includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically deploys to Arcade when:

- **Semver tags** are pushed (e.g., `v1.0.0`, `v2.1.3`, `v1.0.0-beta.1`)
- **GitHub releases** are published

#### Setup Requirements

1. **Add Repository Secret**: In your GitHub repository, go to Settings → Secrets and variables → Actions, and add:
   - **Name**: `ArcadeApiKey`
   - **Value**: Your Arcade API key

2. **Create a Release**:

   ```bash
   # Create and push a semver tag
   git tag v0.1.0
   git push origin v0.1.0

   # Or create a GitHub release
   gh release create v0.1.0
   ```

The workflow will automatically run `arcade deploy` and provide deployment status information.

See [Arcade's deployment documentation](https://docs.arcade.dev/home/serve-tools/arcade-deploy) for more information along with the `deploy` usage [guide](https://docs.arcade.dev/home/arcade-cli#arcade-deploy).

## 🏆 Outcome

I feel all of the [project goals](#-project-goals) were achieved. I was able to successfully deploy my worker to Arcade.dev using Cloudflare and test via the dashboard tool calling interface.

Worker URI: `https://e58rbgi8n1svd5mpt8rxtr316-1972021761134002131.server.arcade.dev`
Secret: `<default suggestion>`

_It is unclear to me the best way to provide the information necessary for others to interface with this toolkit... the [deploy documentation](https://docs.arcade.dev/home/serve-tools/arcade-deploy) does not include information on this._

## Next Steps

With the solid foundation established, future enhancements could include:

- **More Tools** - Use more of the Found Audio api to do things like leave comment or favorite (from authenticated state)
- **User Auth** - Add tools that require Found Audio user authentication, eg post comments and like audio files
- **Caching Layer** - To prevent having to call the external API all the time
- **Monitoring** - Metrics, observability, alerting

## Additional Resources

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
