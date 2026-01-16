# 🏦 System Architecture: Presentation Guide (Ultra-Detailed)

This guide is designed for your **first time** explaining this architecture. It covers exactly what each block is and *why* it exists.

---

## 1. The Strategy: "The Big Picture"
*Start your explanation with this:*
"Our system is an **Intelligent Event-Driven Platform**. It doesn't just sit and wait; it listens to customer behavior on shopping websites and reacts instantly using AI to recover lost sales."

---

## 2. Block-by-Block Breakdown (What is What?)

### **Section A: User Inputs (The Source)**
*   **Merchant Dashboard**: This is the "Control Room." The business owner logs in here to see how much money the AI has recovered.
*   **Customer (End User)**: This is the person browsing the website. They are the ones who might receive our AI phone call.
*   **Shopify/Storefront**: The source of our data. Whenever someone "Adds to Cart," Shopify sends us a notification.

### **Section B: Data Ingestion (The Senses)**
*   **Webhook Handler**: Imagine this as a 24/7 gatekeeper. It catches thousands of "Cart Abandoned" signals every second.
*   **Data Transformation**: This "translates" the data. It ensures that whether the store is Shopify, WooCommerce, or Magento, the rest of our system sees it in one single, clean format.

### **Section C: Data in Motion (The Highway)**
*   **Event Backbone (Redis Streams)**: This is a high-speed highway that moves data between different parts of the platform. It ensures the AI is triggered in **milliseconds**, not minutes after a customer leaves.

### **Section D: Intelligent Application (The Brain)**
*   **BFF - Orchestration Layer**: The conductor of the orchestra. It talks to all the other AI tools and ensures they work together.
*   **Decision Service**: The "Rule Maker." It checks criteria like: *"Is the cart worth more than $50?"* or *"Has this customer already been called today?"*
*   **NLP Services (LLM & RAG)**: This is where "Knowledge" lives. It uses GPT models and a "Product Knowledge Base" so the AI doesn't hallucinate and knows exactly what products the customer left behind.
*   **Speech Execution**: This is the "Voice." It handles the phone call or SMS using tools like Vapi or Twilio.

---

## 3. The Live Flow (Follow the Arrows)
*Walk the audience through this path:*
1.  **Event happens**: Customer leaves the Shopify store.
2.  **Signal caught**: Webhook Handler catches it.
3.  **Data moved**: Event Backbone carries it to the Orchestrator.
4.  **Decision made**: Decision Service says, "Yes, let's call this customer!"
5.  **AI talks**: Speech Execution calls the Customer.
6.  **Results stored**: Everything is saved into the Storage layer.

---

## 4. Tough Questions & Answers (Be Prepared!)
*   **Q: Why do we need an 'Event Backbone'?**
    *   *A: "It allows the system to be 'Asynchronous.' If the AI service is busy, the backbone holds several events in a queue so we never lose a customer lead."*
*   **Q: Can we change the AI model (like from GPT-4 to Gemini)?**
    *   *A: "Yes! Because we use a 'BFF-Orchestration' layer, we can swap any internal service without changing the whole architecture."*
