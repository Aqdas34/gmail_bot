# Bot Working Guide  

## Overview  
This bot automates the creation of email accounts using data from an Excel file. The file should contain the following columns:  
- **Age**  
- **Name**  
- **Surname**  
- **Gender**  
- **Date of Birth**  

## How It Works  

1. **Launching the Bot**  
   - When you start the bot, a small GUI window appears.  
   - You need to select the Excel file containing user data.  

2. **Input Requirements**  
   - After selecting the Excel file, provide:  
     - A password for the email accounts.  
     - The number of emails to create.  
     - A recovery email  
     - A proxy (optional) in the format: `host:port:username:password`.  

3. **Bot Execution**  
   - Once started, the bot will:  
     - Automatically fill in the required fields.  
     - Use daily SMS verification for phone numbers (**$0.20 per number**).  

4. **Saving Account Details**  
   - After successful email creation, the bot updates the same Excel file by:  
     - Adding the email, password, and recovery email.  
     - Marking the account creation status in a new **"done"** column with a value of `1`.  

5. **Unique Email Generation**  
   - Each email is generated uniquely using a combination of:  
     - **Name + Surname + Period + Numbers**.  

## Additional Notes  
- Ensure you have sufficient balance for SMS verification.  
- Proxy usage is optional but recommended for better anonymity.  
- The bot ensures smooth automation with minimal user input.  
