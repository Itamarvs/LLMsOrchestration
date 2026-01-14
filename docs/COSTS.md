# Cost & Token Analysis

## Overview
This document outlines the API costs and token usage for the Deepfake Detection System using Google's Gemini API.

## Gemini API Pricing (as of 2026-01)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Gemini 1.5 Flash | $0.075 | $0.30 |
| Gemini 1.5 Pro | $1.25 | $5.00 |

> **Note**: We use `gemini-flash-latest` for cost efficiency while maintaining quality.

## Token Usage per Analysis

| Component | Estimated Tokens |
|-----------|-----------------|
| System Prompt (Forensic Persona) | ~500 tokens |
| Image Frames (3 frames × ~1000 tokens each) | ~3,000 tokens |
| Model Response | ~200 tokens |
| **Total per Analysis** | **~3,700 tokens** |

## Cost per Video Analysis

Using Gemini 1.5 Flash:
- **Input cost**: 3,500 tokens × $0.075 / 1M = **$0.000263**
- **Output cost**: 200 tokens × $0.30 / 1M = **$0.00006**
- **Total per video**: **~$0.0003** (less than 1 cent)

## Budget Optimization Strategies

1. **Frame Reduction**: Analyze 3 frames instead of 10+ (reduces tokens by 70%)
2. **Caching**: Cache prompts that don't change between requests
3. **Batch Processing**: Group multiple videos when possible
4. **Mock Mode**: Use mock mode for development/testing (0 cost)

## Monthly Cost Projections

| Videos/Month | Estimated Cost |
|--------------|----------------|
| 100 | $0.03 |
| 1,000 | $0.30 |
| 10,000 | $3.00 |

## Rate Limits

| Tier | Requests per Minute | Tokens per Minute |
|------|---------------------|-------------------|
| Free | 2 RPM | 32,000 TPM |
| Tier 1 | 60 RPM | 1,000,000 TPM |

> **Implementation**: Our system includes exponential backoff retry logic to handle `429 Resource Exhausted` errors gracefully.
