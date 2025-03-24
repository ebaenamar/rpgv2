import json
import os
from typing import List, Dict, Any, Optional

class RAGRetriever:
    def __init__(self, index_path: str, documents_path: str):
        # In a full implementation, we would use FAISS or another vector database
        # For this MVP, we'll use a simple in-memory approach with sample data
        self.documents = self._load_sample_documents()
        
    def _load_sample_documents(self) -> List[Dict[str, Any]]:
        """Load sample historical documents"""
        return [
            {
                "title": "Medieval English Village Life",
                "text": "In 13th century England, villages were typically centered around a church and manor house. Most villagers were serfs who worked the lord's land in exchange for protection and the right to farm small plots for themselves. Daily life revolved around agricultural work, with different tasks depending on the season. Village communities were close-knit, with social gatherings often occurring after church services on Sundays.",
                "tags": ["England", "village", "daily life", "13th century"],
                "region": "England"
            },
            {
                "title": "Medieval Church and Religion",
                "text": "The church was the center of medieval life, both spiritually and socially. Church bells marked the hours of the day and called people to prayer. Priests were often the most educated people in a village and served as advisors and record-keepers. Most people were deeply religious, believing firmly in heaven, hell, and the power of saints to intercede on their behalf. Churches often contained relics believed to have healing powers.",
                "tags": ["religion", "church", "priest", "medieval"],
                "region": "Europe"
            },
            {
                "title": "Medieval Taverns and Alehouses",
                "text": "Taverns in medieval England served as important social hubs where people gathered to drink, share news, and find lodging. Ale was the common drink, as water was often unsafe. Tavern keepers were licensed by local authorities and had to follow regulations about prices and measures. Travelers often sought out taverns for accommodation, though they might have to share beds with strangers. Gambling, storytelling, and music were common tavern entertainments.",
                "tags": ["tavern", "ale", "social", "England", "medieval"],
                "region": "England"
            },
            {
                "title": "Medieval Forests and Wilderness",
                "text": "Forests in medieval England were not simply wild areas but legally designated regions subject to forest law, which preserved hunting rights for the nobility. Commoners could be severely punished for poaching. However, forests provided essential resources: wood for fuel and building, herbs for medicine, honey from wild bees, and forage for pigs. Outlaws sometimes lived in forests, giving rise to legends like Robin Hood. Travelers feared forests as places of danger and mystery.",
                "tags": ["forest", "wilderness", "medieval", "England"],
                "region": "England"
            },
            {
                "title": "Village Elders and Governance",
                "text": "In medieval English villages, elders were respected community members who helped resolve disputes and maintain local customs. While the lord's steward had official authority, village elders often had significant informal influence. Many served on manorial courts that handled minor offenses and land disputes. Village elders were typically older men who had demonstrated wisdom and fairness throughout their lives. Some were also skilled in traditional medicine, using herbs and folk remedies to treat common ailments.",
                "tags": ["elder", "governance", "village", "medieval", "England"],
                "region": "England"
            },
            {
                "title": "Medieval Knights and Chivalry",
                "text": "Knights in 13th century England were mounted warriors who served a lord in exchange for land (fiefs). The code of chivalry governed knightly behavior, emphasizing courage, loyalty, and protection of the weak. Knights underwent years of training, starting as pages around age 7, then becoming squires before being knighted. A knight's armor and weapons were extremely expensive, often costing the equivalent of several years' income from a manor. Tournaments allowed knights to practice combat skills and gain reputation.",
                "tags": ["knight", "chivalry", "medieval", "England", "13th century"],
                "region": "England"
            }
        ]
        
    def retrieve(self, query: str, k: int = 2, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieve relevant documents based on query and optional filters"""
        # In a full implementation, this would use vector similarity search
        # For this MVP, we'll use simple keyword matching
        
        # Convert query to lowercase for case-insensitive matching
        query_lower = query.lower()
        
        # Split query into keywords
        keywords = query_lower.split()
        
        # Score documents based on keyword matches
        scored_docs = []
        for doc in self.documents:
            # Apply filters if provided
            if filters:
                skip = False
                for key, value in filters.items():
                    if key in doc and value is not None and doc[key] != value:
                        skip = True
                        break
                if skip:
                    continue
            
            # Count keyword matches in title and text
            score = 0
            for keyword in keywords:
                if keyword in doc["title"].lower():
                    score += 2  # Title matches are weighted higher
                if keyword in doc["text"].lower():
                    score += 1
                if "tags" in doc:
                    for tag in doc["tags"]:
                        if keyword in tag.lower():
                            score += 1.5  # Tag matches are also important
            
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score (descending) and take top k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        top_docs = [doc for score, doc in scored_docs[:k]]
        
        return top_docs
