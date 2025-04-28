import sys
import json
import requests
from datetime import datetime
from flowlauncher import FlowLauncher

class NotionFlowLauncher(FlowLauncher):
    # Notion API constants
    NOTION_API_URL = "https://api.notion.com/v1"
    
    def __init__(self):
        # Load your Notion API token and database ID from settings
        self.notion_token = "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"  # Replace with your actual token
        self.database_id = "ec96c591108e4637a9644c8d3460d5f2"  # Replace with your actual database ID
        
    def query(self, query):
        # If the query is empty, return basic info
        if not query:
            return [
                {
                    "Title": "Add to Notion",
                    "SubTitle": "Type text to add as a new page in your Notion database",
                    "IcoPath": "Images\\notion_icon.png"
                }
            ]
        
        # If there's a query, provide option to add it to Notion
        return [
            {
                "Title": f"Add to Notion: {query}",
                "SubTitle": "Press Enter to add this as a new page",
                "IcoPath": "Images\\notion_icon.png",
                "JsonRPCAction": {
                    "method": "add_to_notion",
                    "parameters": [query]
                }
            }
        ]
    
    def add_to_notion(self, query):
        try:
            # Create page in Notion database
            success = self._create_notion_page(query)
            
            if success:
                return [
                    {
                        "Title": "Added to Notion!",
                        "SubTitle": f"Successfully added: {query}",
                        "IcoPath": "Images\\notion_success.png"
                    }
                ]
            else:
                return [
                    {
                        "Title": "Failed to add to Notion",
                        "SubTitle": "There was an error. Check your API token and database ID.",
                        "IcoPath": "Images\\notion_error.png"
                    }
                ]
        except Exception as e:
            return [
                {
                    "Title": "Error",
                    "SubTitle": f"Error: {str(e)}",
                    "IcoPath": "Images\\notion_error.png"
                }
            ]
    
    def _create_notion_page(self, content):
        """Create a new page in Notion database with the provided content"""
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"  # Update this if there's a newer version
        }
        
        # Get current date/time for the created timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Customize this request based on your database properties
        # This assumes your database has "Name" and "Created" properties
        data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": content
                            }
                        }
                    ]
                },
                "Created": {
                    "date": {
                        "start": current_time
                    }
                }
            }
        }
        
        # You can add more properties or content to the page here
        
        # Make the API request
        response = requests.post(
            f"{self.NOTION_API_URL}/pages",
            headers=headers,
            json=data
        )
        
        # Check if the request was successful
        return response.status_code == 200

if __name__ == "__main__":
    NotionFlowLauncher()
