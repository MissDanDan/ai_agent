graph TB
    subgraph External["External Services"]
        OpenAI[OpenAI/LLM Gateway]
        GaaS[GaaS - Content Filtering]
        IDP[Identity Provider - Authentication]
    end
    
    subgraph Infrastructure["Infrastructure Layer"]
        Docker[Docker Swarm - Container Orchestration]
        Traefik[Traefik - Reverse Proxy]
    end
    
    subgraph AgentRuntime["Agent Runtime"]
        AIAgent[AI Agents - BaseAgent Implementation]
        Langfuse[Langfuse - Observability]
        Memory[Memory Systems - PostgreSQL/In-Memory]
        MCP[MCP Servers - Tool Providers]
    end
    
    subgraph Development["Development Layer"]
        DevUI[Development UI - React Dashboard]
        FastAPI[FastAPI Backend - Port 8000]
        NXTemplates[NX Templates - Code Generation]
    end
    
    subgraph SDK["SDK Layer"]
        CommonSDK[ABK Common SDK - Core Abstractions]
        OpenAISDK[ABK OpenAI SDK - OpenAI Integration]
        PydanticSDK[ABK Pydantic AI SDK - Pydantic Integration]
    end
    
    PostgresDB[(PostgreSQL - Data Storage)]
    
    Docker --> Traefik
    Traefik --> AIAgent
    
    OpenAI --> AIAgent
    GaaS --> AIAgent
    IDP --> AIAgent
    
    AIAgent --> Langfuse
    AIAgent --> Memory
    AIAgent --> MCP
    AIAgent --> FastAPI
    
    Langfuse --> PostgresDB
    Memory --> PostgresDB
    
    FastAPI --> DevUI
    FastAPI --> NXTemplates
    
    MCP --> CommonSDK
    NXTemplates --> CommonSDK
    
    CommonSDK --> OpenAISDK
    CommonSDK --> PydanticSDK
    
    style External fill:#f9f7e8
    style Infrastructure fill:#f9f7e8
    style AgentRuntime fill:#f9f7e8
    style Development fill:#f9f7e8
    style SDK fill:#f9f7e8
