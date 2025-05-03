When designing tools for the AI make sure to 
- always return a response, event a simple one, even if the response is empty
- NEVER THROW AN ERROR, just return the error and log it
- make sure to follow the types defined in the route of the API
- make sure to name them consistently
- add the new tools to the tools list (app/(chat)/api/chat/route.ts)
- add also the string names of the tools to the tools list (app/(chat)/api/chat/route.ts)

When creating a new tool in the UI, to do change (create, update, delete) the tool in the UI, make a UI, pop-up to show the result of the tool (frontend/components/bunq/TOOL-NAME.tsx)
- it should be a simple card to display the most important information
- there should be a loading state
- there should be a success state
- there should be an error state (in case there are details in the resulf of the tool)
- A LIST SHOULD BE DISPLAYED AS A COMPACT LIST WITH EVEN LESS INFORMATION, SMALLER TEXT, AND A SMALLER CARD, IT SHOULD BE SCROLLABLE IF THERE ARE MORE THAN 5 ITEMS
- the results of the tools are sometimes different, so call the tools using the curl API (http://localhost:8080/...). Be smart about it, sometimes you need one tool to call another tool, so make sure to do that
- add the componenets to the UI render list (frontend/components/message.tsx)