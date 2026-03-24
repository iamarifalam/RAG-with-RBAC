---
layout: default
title: Home
---

<div class="hero-section">
  <div class="container">
    <h1 class="hero-title">Atlas: Enterprise Knowledge Assistant</h1>
    <p class="hero-subtitle">Secure, Intelligent Document Retrieval with Role-Based Access Control</p>
    <div class="hero-buttons">
      <a href="#demo" class="btn btn-primary">View Live Demo</a>
      <a href="#features" class="btn btn-secondary">Explore Features</a>
    </div>
  </div>
</div>

<section id="overview" class="section">
  <div class="container">
    <h2>Enterprise-Grade RAG System</h2>
    <p>Atlas transforms your organization's knowledge base into an intelligent, secure assistant. Built with production-ready architecture, it combines advanced retrieval-augmented generation with comprehensive access controls to deliver accurate, compliant responses.</p>
    
    <div class="stats-grid">
      <div class="stat">
        <h3>99.9%</h3>
        <p>Uptime SLA</p>
      </div>
      <div class="stat">
        <h3>&lt;100ms</h3>
        <p>Response Time</p>
      </div>
      <div class="stat">
        <h3>100%</h3>
        <p>Role Compliance</p>
      </div>
    </div>
  </div>
</section>

<section id="features" class="section section-alt">
  <div class="container">
    <h2>Core Capabilities</h2>
    <div class="features-grid">
      <div class="feature-card">
        <div class="feature-icon">🔒</div>
        <h3>Role-Based Access Control</h3>
        <p>Multi-layer security ensures users only access authorized information. Domain-specific filtering prevents data leakage while maintaining productivity.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <h3>Advanced RAG Engine</h3>
        <p>BM25-powered retrieval with semantic understanding delivers precise, context-aware responses from your document corpus.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Comprehensive Monitoring</h3>
        <p>Built-in metrics, audit trails, and performance monitoring ensure reliability and compliance in production environments.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3>High Performance</h3>
        <p>Async FastAPI backend with optimized indexing and caching delivers sub-second responses at scale.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🛡️</div>
        <h3>Enterprise Security</h3>
        <p>JWT authentication, input validation, and content filtering protect against unauthorized access and malicious inputs.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🐳</div>
        <h3>Container Ready</h3>
        <p>Docker deployment with multi-stage builds ensures consistent, secure delivery across development and production.</p>
      </div>
    </div>
  </div>
</section>

<section id="demo" class="section">
  <div class="container">
    <h2>Interactive Demo</h2>
    <p>Experience Atlas in action with our live demonstration. Use the demo credentials below to explore role-based knowledge access:</p>
    
    <div class="demo-credentials">
      <div class="credential-card">
        <h4>Finance Executive</h4>
        <p><strong>Username:</strong> alice.finance</p>
        <p><strong>Password:</strong> FinanceDemo123</p>
        <p>Access: Financial documents and budgets</p>
      </div>
      <div class="credential-card">
        <h4>HR Manager</h4>
        <p><strong>Username:</strong> harry.hr</p>
        <p><strong>Password:</strong> HRDemo123</p>
        <p>Access: HR policies and payroll information</p>
      </div>
      <div class="credential-card">
        <h4>Executive</h4>
        <p><strong>Username:</strong> erin.exec</p>
        <p><strong>Password:</strong> ExecDemo123</p>
        <p>Access: All enterprise documents</p>
      </div>
    </div>
    
    <div class="demo-link">
      <a href="https://atlas-demo.yourdomain.com" class="btn btn-primary" target="_blank">Launch Live Demo</a>
    </div>
  </div>
</section>

<section id="architecture" class="section section-alt">
  <div class="container">
    <h2>System Architecture</h2>
    <div class="architecture-diagram">
      <img src="assets/architecture-diagram.png" alt="Atlas System Architecture" style="max-width: 100%; height: auto;">
    </div>
    <p>Built with modern Python stack: FastAPI, Pydantic, BM25, JWT, and comprehensive testing suite.</p>
  </div>
</section>

<section id="deployment" class="section">
  <div class="container">
    <h2>Production Deployment</h2>
    <div class="deployment-options">
      <div class="deploy-card">
        <h3>Docker Container</h3>
        <pre><code>docker-compose up -d</code></pre>
        <p>Single-command deployment with all dependencies</p>
      </div>
      <div class="deploy-card">
        <h3>Cloud Platforms</h3>
        <p>Azure, AWS, GCP ready with infrastructure as code</p>
      </div>
      <div class="deploy-card">
        <h3>On-Premises</h3>
        <p>Secure deployment behind corporate firewalls</p>
      </div>
    </div>
  </div>
</section>