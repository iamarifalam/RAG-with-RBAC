---
layout: default
title: Home
---

<div class="hero-section">
  <div class="container">
    <h1 class="hero-title">Atlas: Enterprise Knowledge Assistant</h1>
    <p class="hero-subtitle">Secure RAG system with role-based access control for internal company docs</p>
    <div class="hero-buttons">
      <a href="#demo" class="btn btn-primary">Try Demo</a>
      <a href="https://github.com/iamarifalam/RAG-with-RBAC" class="btn btn-secondary">View Code</a>
    </div>
  </div>
</div>

<section id="overview" class="section">
  <div class="container">
    <h2>What is Atlas?</h2>
    <p>I built Atlas to solve a real problem: how do you safely give employees access to company knowledge without risking data leaks or compliance issues? It's like Google for your internal docs, but with security built-in from the ground up.</p>

    <div class="features-grid">
      <div class="feature-card">
        <h3>Role-Based Security</h3>
        <p>Finance sees finance docs, HR sees HR docs. No more accidentally sharing sensitive information.</p>
      </div>
      <div class="feature-card">
        <h3>Guardrails First</h3>
        <p>Checks questions before hitting the LLM. Prevents hallucinations and blocks inappropriate queries.</p>
      </div>
      <div class="feature-card">
        <h3>Full Audit Trail</h3>
        <p>Every question and answer is logged. Perfect for compliance and investigations.</p>
      </div>
    </div>
  </div>
</section>

<section id="demo" class="section section-alt">
  <div class="container">
    <h2>Try It Out</h2>
    <p>The demo is running live. Use these credentials to see how role-based access works:</p>

    <div class="demo-credentials">
      <div class="credential-card">
        <h4>Finance Analyst</h4>
        <p><strong>alice.finance</strong> / FinanceDemo123</p>
        <p>Can access: Finance docs + policies</p>
      </div>
      <div class="credential-card">
        <h4>HR Manager</h4>
        <p><strong>harry.hr</strong> / HRDemo123</p>
        <p>Can access: HR docs + policies</p>
      </div>
      <div class="credential-card">
        <h4>Executive</h4>
        <p><strong>erin.exec</strong> / ExecDemo123</p>
        <p>Can access: Everything</p>
      </div>
    </div>

    <p><strong>Try asking:</strong> "What's in the Q3 budget?" as different users to see the security in action.</p>

    <div class="demo-link">
      <a href="https://atlas-demo.yourdomain.com" class="btn btn-primary">Launch Demo</a>
    </div>
  </div>
</section>

<section id="tech" class="section">
  <div class="container">
    <h2>How It Works</h2>
    <p>Built with Python, FastAPI, and BM25 search. Simple but effective architecture:</p>
    <ul>
      <li><strong>Auth:</strong> JWT tokens with role claims</li>
      <li><strong>Guardrails:</strong> Pre-LLM filtering for security</li>
      <li><strong>Retrieval:</strong> BM25 keyword search over documents</li>
      <li><strong>LLM:</strong> Pluggable backends (mock or OpenAI)</li>
      <li><strong>Monitoring:</strong> Prometheus metrics and structured logs</li>
    </ul>
  </div>
</section>