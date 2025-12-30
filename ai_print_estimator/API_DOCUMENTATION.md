## 📑 Technical Documentation

This section provides API documentation, database schema, and workflow automation details as requested.

---

## 🔗 API Documentation (Swagger / OpenAPI)

The backend exposes REST APIs documented using **Swagger (OpenAPI)**.

Once the application is running, the interactive API documentation is available at:

- **Swagger UI:**  
  http://localhost:8000/docs

These endpoints allow recruiters and developers to:
- Explore all available APIs
- View request/response schemas
- Test APIs directly from the browser

---

## 🗄️ Database Schema

> **Current State:**  
This project is designed with a **pluggable database architecture**.  
At present, the pricing logic operates without a persistent database to keep estimation fast and stateless.

### Planned / Reference Schema (for production use)

```sql
TABLE print_jobs (
    id UUID PRIMARY KEY,
    width FLOAT NOT NULL,
    height FLOAT NOT NULL,
    material VARCHAR(50),
    quantity INT,
    finishing_options JSON,
    estimated_cost FLOAT,
    created_at TIMESTAMP
);

TABLE pricing_rules (
    id UUID PRIMARY KEY,
    material VARCHAR(50),
    base_rate FLOAT,
    ai_modifier FLOAT,
    updated_at TIMESTAMP
);
```
