# AI SQL Assistant 🤖

An AI-powered SQL assistant that translates natural language questions into SQL queries and provides easy-to-understand results from your database.


## Features

- 🗣️ Ask questions about your database in plain English
- 📊 Get results as clean, readable tables
- 🔍 Understands complex database relationships
- 🧠 Transparent reasoning process
- 🖥️ Available as CLI only currently 

## Requirements

- Python 3.8+
- A MySQL database
- A [Groq](https://groq.com) API key (free tier available)
- Any company api key would work, not specifically groq, i use it because it is free. You can use either GEMINI, OPENAI, TOGETHER-AI, OPEN-router or any other, there are many you can even use your locally hosted models using ollama, You just need to adjust the openai wrapper accordingly. 
- I would recommend using groq since it works for me. 

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/Knightride1/SQL-cli-agent
cd SQL-cli-agent
```

2. **Create and activate a virtual environment**

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up your environment variables**

Create a `.env` file in the project directory with the following content:

```
GROQ_API_KEY="your_groq_api_key_here"
```

You can obtain a Groq API key by signing up at [https://console.groq.com/](https://console.groq.com/)

## Usage

### CLI Version

Run the CLI version with:

```bash
python sql_assistant_cli.py
```

Example interaction:
```
> What departments have the highest budgets?
🧠: I need to understand the database schema first.
⚡: Using get_schema with input: 
👁️: {"department": [{"Field": "dept_name", "Type": "varchar(20)"}, {"Field": "building", "Type": "varchar(15)"}, {"Field": "budget", "Type": "numeric(12,2)"}], ...}
🧠: I'll query the department table and sort by budget in descending order.
⚡: Using run_sql_query with input: SELECT dept_name, budget FROM department ORDER BY budget DESC LIMIT 5
👁️: Executed Query:
SELECT dept_name, budget FROM department ORDER BY budget DESC LIMIT 5

Results:
dept_name | budget
---------------------
Finance   | 120000.00
Physics   | 93000.00
Music     | 80000.00
History   | 50000.00
Biology   | 42000.00

🤖: The department with the highest budget is Finance with $120,000, followed by Physics with $93,000 and Music with $80,000.
```



## Database Setup

This assistant works with any MySQL database. If you want to use the university database example:

1. Create a database named "university"
2. Run the setup script to create tables and populate data:

```bash
mysql -u yourusername -p university < database/university_setup.sql
```

## Customizing the Code

### Changing the Model

You can change the LLM model by updating the model parameter in the code:

```python
# In CLI version
response = client.chat.completions.create(
    model="your-preferred-model",  # Change this line
    response_format={"type": "json_object"},
    messages=messages
)



### Supporting Other Databases

To support databases other than MySQL, modify the connection and query functions in the code.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Groq](https://groq.com) and [Llama 4](https://ai.meta.com/llama/) models
- Inspired by the database examples from the Korth database textbook
