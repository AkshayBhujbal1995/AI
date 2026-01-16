# 🗄️ Database Schema: Presentation Guide (Ultra-Detailed)

This guide explains your database in a way that shows **Sales Intelligence** and **Technical Depth**.

---

## 1. The Strategy: "The Memory"
*Start your explanation with this:*
"Our database is more than just storage; it is a **Customer Intelligence Vault**. We track every single nuance of the customer's journey, from what they liked to why they hesitated during checkout."

---

## 2. Table-by-Table Breakdown (What is What?)

### **The Core Hierarchy**
*   **Merchant & Store**: These define **Who** owns the data. It's built for "Multi-tenancy," meaning one merchant can run 10 different stores, and all data remains perfectly separated and secure.
*   **Customer**: Stores the persistent identity. We track **Lifetime Value** here to identify our VIP customers.

### **The Shopping Logic**
*   **Cart & Cart_Item**: This is the "What." We don't just know they left; we know they left with a *Blue Hoodie, size Large, priced at $45*. This detail makes the AI call feel personal and human.

### **The AI Intelligence (Crucial Section!)**
*   **Interaction**: This is our "Master Intelligence" table. Unlike simple logs, it captures:
    *   **Sentiment & Emotion**: Was the customer happy, frustrated, or confused?
    *   **Primary Intent**: Did they actually want to buy, or were they just browsing?
    *   **Objections**: What stopped them? (e.g., "Shipping cost," "Size availability," "Price").
*   **Conversation**: Stores the full **Transcript**. This is our audit trail. If a merchant wants to know exactly what the AI said, it's all here.

### **The Success Tracking (ROI)**
*   **Incentive**: Shows what "carrots" we used to close the deal (e.g., 10% discount).
*   **Order_Log**: The finish line. We mark orders as **Recovered** to prove our platform's value.

---

## 3. The Logical Flow (The Data Journey)
*Walk them through it:*
1.  **Merchant** sets up a **Store**.
2.  **Customer** enters the Store and adds items to a **Cart**.
3.  When the Cart is abandoned, an **Interaction** is triggered.
4.  The AI analyzes the call to generate **Conversation** data, **Sentiment**, and **Objections**.
5.  If the customer buys, an **Order_Log** is created, and the revenue is attributed back to that call!

---

## 4. Tough Questions & Answers (Be Prepared!)
*   **Q: Why do we have separate 'Interaction' and 'Conversation' tables?**
    *   *A: "Separation of concerns. 'Interaction' handles the meta-data (status, scores, timing), while 'Conversation' handles the heavy text data (transcripts). This makes the database much faster to search."*
*   **Q: How do we track 'Sentiment' and 'Objections'?**
    *   *A: "Our AI (NLP Services) parses the call transcript in real-time and populates these fields automatically using structured data extraction."*
*   **Q: Why store 'Timezone'?**
    *   *A: "To ensure we never call a customer at 3 AM. It's built for global compliance and respect for the customer's time."*
