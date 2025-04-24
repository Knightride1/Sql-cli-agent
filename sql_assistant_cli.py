from dotenv import load_dotenv
import os
import json
import mysql.connector
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Database tools
def get_schema(_: str = ""):
    """Retrieves the database schema including tables and columns."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="#your sql username#",
            password="#your passwor#",
            database="#your database name#"
        )
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        schema = {}

        for (table_name,) in tables:
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            schema[table_name] = [{"Field": col[0], "Type": col[1]} for col in columns]

        cursor.close()
        connection.close()
        return json.dumps(schema, indent=2)
    except Exception as e:
        return f"Error retrieving schema: {str(e)}"

def run_sql_query(query):
    """Executes a SQL query and returns formatted results."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="#your sql username#",
            password="#your passwor#",
            database="#your database name#"
        )
        cursor = connection.cursor()
        cursor.execute(query)
        
        # Get results and column names
        results = cursor.fetchall()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        
        cursor.close()
        connection.close()
        
        # Format results as a table
        result_table = []
        
        # Add header row
        if columns:
            result_table.append(" | ".join(columns))
            result_table.append("-" * (sum(len(col) for col in columns) + 3 * (len(columns) - 1)))
        
        # Add data rows
        for row in results:
            result_table.append(" | ".join(str(item) for item in row))
            
        formatted_output = f"Executed Query:\n{query}\n\nResults:\n"
        if result_table:
            formatted_output += "\n".join(result_table)
        else:
            formatted_output += "No results found."
            
        return formatted_output
    except Exception as e:
        return f"Error executing query: {str(e)}"

# Define available tools
available_tools = {
    "get_schema": {
        "fn": get_schema,
        "description": "Takes no input and retrieves the database schema including tables and columns."
    },
    "run_sql_query": {
        "fn": run_sql_query,
        "description": "Takes a SQL query as input, executes it, and returns formatted results."
    }
}

# System prompt
system_prompt = f"""
You are a MySQL database assistant that helps users retrieve information from a database.
You work in start, plan, action, observe mode.

For the given user query and available tools, plan the step by step execution.
Based on the planning, select the relevant tool from the available tools.
And based on the tool selection you perform an action to call the tool.
Wait for the observation and based on the observation from the tool call, resolve the user query.

Rules:
1. Follow the strict JSON output as per output schema
2. Always perform one step at a time and wait for next input
3. Always get the schema first before writing any SQL query
4. Write clear, efficient SQL queries
5. Explain the results in plain language

Output JSON format:
{{
    "step": "string",
    "content": "string",
    "function": "the name of the function if the step is the action",
    "input": "The input parameter for the function"
}}

Available Tools:
- get_schema: {available_tools['get_schema']['description']}
- run_sql_query: {available_tools['run_sql_query']['description']}

Example:
User Query: What tables are in the database?
Output: {{"step": "plan", "content": "I need to retrieve the database schema to see what tables are available."}}
Output: {{"step": "action", "function": "get_schema", "input": ""}}
Output: {{"step": "observe", "output": "Tables: students, courses, professors..."}}
Output: {{"step": "output", "content": "The database contains the following tables: students, courses, professors..."}}
"""

messages = [
    {"role": "system", "content": system_prompt}
]

# Main interaction loop
while True: 
    query = input("> ")
    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            response_format={"type": "json_object"},
            messages=messages
        )
        parsed_response = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_response)})

        step = parsed_response.get("step")
        
        if step == "plan":
            print(f"🧠: {parsed_response.get('content')}")
            continue
            
        elif step == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input", "")

            if tool_name in available_tools:
                print(f"⚡: Using {tool_name} with input: {tool_input}")
                output = available_tools[tool_name]["fn"](tool_input)
                messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                print(f"👁️: {output}")
                continue
            else:
                print(f"❌: Unknown tool: {tool_name}")
                break
                
        elif step == "output":
            print(f"🤖: {parsed_response.get('content')}")
            break
            
        else:
            print(f"⚠️: Invalid step: {step}")
            break