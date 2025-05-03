# Project Overview

Name: Yet Another AI Agent.

Elevator Pitch: 
```
Turn plain language into instant action. Your money works smarter, effortlessly. 
Manage tasks, settings, and budgets, alerts you before overspending, and even split bills.
```
# Project Details

## About the Project

### Inspiration

Our project was inspired by the problems below:
- **Time Wasted Navigating**: Users waste time navigating the app to do basic tasks.
- **Lack of Real-Time Financial Awareness**: Users often make spending decisions without understanding the impact on their budget, leading to overspending or regret.
- **Difficulty Making Budget-Friendly Choices**: It's hard for users to evaluate spending options in everyday situations, like dining out, without context-aware financial insight.

### What it does

Our YAAI Agent: 
- Understands natural language
- Executes actions such as payments, info requests, and contact lookup
- Provides real-time context-aware financial insights

You can ask him, in natural language, how much money you have, to send or receive money, about different transactions, even split the bill with a friend.

### How we built it

To build YAAI Agent, we leaned heavily on existing tools and frameworks that helped us move fast without reinventing the wheel.

We used the AI SDK, which gave us a standardized interface for working with various LLM APIs. It also came with built-in support for agents, tool execution, and memory/context persistence (MCP) out of the box—this helped us focus on writing functionality instead of boilerplate.

For the frontend, we used Vercel’s ChatUI template, which gave us a clean, ChatGPT-style UI. It also came bundled with Postgres, Auth, blob storage, and AI tooling—all of which were super helpful. We mainly extended it by building tools (custom backend APIs) the agent could call.

The backend was built using FastAPI, which gave us a clean, async-first structure for defining our endpoints. For interacting with the banking layer, we used the bunq Python SDK. The SDK had decent documentation, and we were able to implement most features without much friction. However, it lacked Pydantic support—so we wrapped it ourselves to make our FastAPI code fully typed and more maintainable.

We wrote prompts for each tool to give the AI enough context about what each one does, when to use them, and how to chain them logically. The system prompt helped tie everything together so that the agent could reason across tools and complete multi-step tasks.

We hosted the app on DigitalOcean, uploading the build manually in the end—after wasting 4+ hours trying (and failing) to get AWS + GitHub Actions + CI/CD working. Let’s call that a skill issue. For blob storage, we used MinIO, a self-hosted S3-compatible option that ChatGPT actually suggested—and it worked well for our needs.

For models, we used a mix of OpenAI’s APIs:
- gpt-4o-mini for image understanding tasks
- gpt-4o for complex reasoning and task chaining
- gpt-4.1-nano for lightweight things like generating chat titles

### Challenges we ran into

While building YAAI Agent, we encountered a few challenges that gave us a deeper appreciation for the complexity of the tools we were using—and gave us ideas for how they could improve.

Working with the bunq Python SDK was mostly smooth, but we did run into a few limitations. Some API objects were missing or undocumented, which made it tricky to understand what certain fields represented. The SDK also lacked support for Pydantic, which would have made it easier to integrate directly into FastAPI. We worked around this by creating our own wrappers to enforce typing and validation.

Authentication was another sticking point. We created an application in the bunq developer portal, but it wasn’t recognized in the sandbox or production environments. Eventually, we were able to retrieve and use our real API key directly from the bunq app, which was a nice workaround, but it highlighted that the developer onboarding could be a bit more intuitive.

We also spent a lot of time trying to set up CI/CD pipelines with GitHub Actions and AWS. After hours of wrestling with configuration issues, we decided to go with a manual deployment to DigitalOcean for the sake of time. While not ideal, this experience reminded us that automation should only be introduced once it's saving more time than it's costing.

Overall, these challenges pushed us to understand our stack more deeply and shaped some of the architecture decisions we made along the way.

### Accomplishments that we're proud of

_Fill in for Mansur and Amir_

### What we learned

_Fill in for Mansur and Amir_

### What's next for YAAI Agent

The next logical step for this project is to:
- Expand functionality
- Test with real users
- Measure impact on CSAT, support volume, engagement


## Built with
_What languages, frameworks, platforms, cloud services, databases, APIs, or other technologies did you use?_


## Links
_Add links where people can try your project or see your code._

## Images & Videos
Create a video demonstrating the project demo. 
Feel free to include images if necessary.

Images are complete

Video is needed.

