# Knowledge Graph Construction Subsystem Architecture

This document describes the flow of a document as entities and relationships are extracted to construct the knowledge graph in Neo4j.

```
Document
   │
   ▼
Entity Extraction
   │
   ▼
Relationship Extraction
   │
   ▼
Graph Builder
   │
   ▼
 Neo4j
```

## Flow Description

1. **Document**: The raw text ingestion source (e.g. document files, wikis, slack chats, incident logs).
2. **Entity Extraction**: The text is parsed by `IEntityExtractor` using NLP or LLM patterns to identify structured entities matching predefined domains:
   - `Person`, `Team`, `Project`, `Service`, `Incident`, `Document`, `Ticket`, `Decision`
3. **Relationship Extraction**: Identified entities are parsed by `IRelationshipExtractor` to trace direct semantic associations or dependency lines matching:
   - `WORKS_ON`, `OWNS`, `CAUSED`, `DISCUSSED_IN`, `REFERENCES`, `DEPENDS_ON`, `CREATED`, `RESOLVED`, `BELONGS_TO`
4. **Graph Builder**: Collects extracted node and edge lists and compiles them into a unified, formatted `GraphDelta` representing the updates to apply.
5. **Neo4j**: The `IGraphStorage` / `Neo4jAdapter` translates the delta package into Cypher query mutations to create, merge, or delete database elements in Neo4j.
