# Development Guide

> Living engineering documentation for CyberByDan AI

---

# Purpose

This document explains the engineering principles used while building
CyberByDan AI.

It is intentionally opinionated.

The goal is to build an AI platform that is:

- maintainable
- modular
- observable
- production-ready
- easy to understand months from now

Every design decision should support one or more of these goals.

---

# Project Philosophy

CyberByDan AI is **not** just an OpenAI wrapper.

It is a complete Retrieval-Augmented Generation (RAG) platform that exposes
multiple interfaces while sharing a single AI engine.

Every interface should behave identically because they all use the same core.

Instead of building several independent bots, we build one intelligent core
with many front ends.

```
                Telegram

                    │

             Open WebUI

                    │

             OpenAI API

                    │

              Future Apps

                    │

          ---------------------

                 Engine

          ---------------------

        Retriever
        Context Builder
        Prompt Builder
        Reranker
        LLM
        Memory

                    │

             Chroma Database
```

---

# Design Principles

## Single Responsibility

Every module should do exactly one thing.

Examples

reader.py

Reads files.

Nothing else.

---

chunker.py

Splits documents.

Nothing else.

---

vectorstore.py

Stores embeddings.

Nothing else.

---

retriever.py

Searches embeddings.

Nothing else.

---

prompt.py

Builds prompts.

Nothing else.

---

engine.py

Coordinates everything.

Never performs retrieval,
prompt engineering,
or model inference itself.

---

# Keep Layers Independent

Every layer communicates only with adjacent layers.

Good

Engine

↓

Retriever

↓

Vector Store

Bad

Engine

↓

ChromaDB

The engine should never know how Chroma works internally.

---

# Configuration

No hardcoded values.

Everything configurable belongs inside

core/config.py

Examples

Model names

Ports

Hostnames

Collection names

Embedding model

API URLs

---

# RAG Pipeline

The current architecture is

Question

↓

Embedding

↓

Vector Search

↓

Distance Filter

↓

Reranker

↓

Context Builder

↓

Prompt Builder

↓

DeepSeek

↓

Answer

Each stage has exactly one responsibility.

---

# Prompt Engineering Rules

The LLM should never be trusted with facts.

Instead

Retriever

↓

Context

↓

Prompt

↓

LLM

The model only explains.

The knowledge comes from documentation.

---

# Retrieval Philosophy

More retrieved chunks does NOT equal better answers.

Good retrieval means

small amount

high relevance

clear context

We prefer

5 excellent chunks

instead of

20 mediocre chunks.

---

# Chunking Philosophy

Chunk size is a balance.

Large chunks

✔ richer context

✔ fewer hallucinations

✖ slower retrieval

✖ more token usage

Small chunks

✔ faster search

✔ cheaper prompts

✖ fragmented knowledge

CyberByDan currently uses medium-sized semantic chunks.

---

# Embedding Philosophy

Embeddings are generated once.

Questions are embedded at runtime.

Similarity is computed inside ChromaDB.

Embeddings should never be regenerated unnecessarily.

---

# Reranking

Vector search finds

approximately relevant

documents.

The reranker improves quality by considering

keyword overlap

section importance

metadata

future recency

future usage frequency

The reranker is deterministic.

The LLM never performs reranking.

---

# Context Builder

The context builder prepares information for the LLM.

Responsibilities

Remove duplicate chunks

Sort logically

Format consistently

Display metadata

Respect token budget

Future versions will dynamically trim context based on remaining tokens.

---

# OpenAI Compatibility

CyberByDan exposes an OpenAI-compatible API.

This allows any OpenAI-compatible client to use the local AI without
modification.

Examples

Open WebUI

LibreChat

Continue.dev

VS Code extensions

Custom applications

Telegram bots

Future mobile apps

---

# Logging Philosophy

Every important operation should be logged.

Examples

startup

shutdown

retrieval

API requests

errors

backup jobs

future agent actions

Logs should explain

what happened

when

why

---

# Error Handling

Fail loudly.

Never silently ignore failures.

Instead

Report

Log

Recover when possible

Exit cleanly otherwise

---

# Documentation Standard

Every module begins with

Purpose

Responsibilities

Pipeline

Examples where appropriate

Public functions must contain

parameters

returns

purpose

This project values readability over cleverness.

---

# Coding Style

Prefer

clear names

short functions

high comments

predictable structure

Avoid

deep nesting

hidden state

magic values

long functions

---

# Future Architecture

The current system is Version 1.

Future improvements include

Memory

Conversation history

Hybrid search

BM25

Cross-Encoder reranking

Streaming responses

Tool calling

Agent framework

Workflow execution

Voice interface

Telegram Assistant

WhatsApp Assistant

MCP integrations

Local GUI

Dashboard

Multi-user authentication

Plugin architecture

---
---

# Development Workflow

Every engineering task follows the same lifecycle.

```
Plan

↓

Implement

↓

Test

↓

Debug

↓

Document

↓

Update State Inventory

↓

Commit

↓

Push
```

A feature is not considered complete until all of these stages have been completed.

This workflow keeps the implementation, documentation, and retrieval knowledge synchronized.

# Engineering Rule

Every new feature must answer

Why does this exist?

What module owns it?

Can another module already do this?

If ownership is unclear,
the architecture should be redesigned before writing code.

---

# Guiding Principle

Build software that future-you can understand in five minutes.

If today's shortcut becomes tomorrow's confusion,
it was not a shortcut.
