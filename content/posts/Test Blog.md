---
title: "My Test Blog Post"
date: 2024-02-10
author: "Erin"
description: "This is a test blog post about software engineering"
tags: ["software", "engineering", "tutorial"]
categories: ["tech"]
draft: false
toc: true
lastmod: 2024-02-10
permalink: posts/test-blog
---
# Test Blog
More Stuff
[My Test Blog Post #2](/blog/test-blog-2)

**Bold**
*italic*

Random Text

[External Link](https://google.com)

```html
<body>
	<h1>Header 1</h1>
	<p>
		Paragraph
	</p>
</body>
```

`inline code` random text here next to it.

## Image - h2
![IMG-20250210021231096.jpeg](/blog/images/IMG-20250210021231096.jpeg)
### PDF - h3
{{< pdf src="/blog/files/IMG-20250210021231508.pdf" >}}

### Canvas - h3

<div class="canvas-container">
<style>
            .canvas-container {
                position: relative;
                width: 100%;
                height: 600px;
                background: var(--background);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                overflow: hidden;
                margin: 1rem 0;
            }
            .canvas-node {
                position: absolute;
                background: var(--background);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 1rem;
                max-width: 300px;
                transition: transform 0.2s;
                z-index: 1;
            }
            .canvas-node:hover {
                transform: translateY(-2px);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                z-index: 2;
            }
            .canvas-node-text {
                font-size: 0.9rem;
                color: var(--color);
                white-space: pre-wrap;
            }
            .canvas-node-file {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .canvas-node-file img {
                max-width: 100%;
                height: auto;
                margin-bottom: 0.5rem;
                border-radius: 4px;
            }
            .canvas-node-file a {
                color: var(--accent);
                text-decoration: none;
            }
            .canvas-node-file a:hover {
                text-decoration: underline;
            }
            .canvas-edge {
                position: absolute;
                height: 2px;
                background: var(--accent);
                opacity: 0.5;
                transform-origin: left center;
                pointer-events: none;
            }
            @media (max-width: 768px) {
                .canvas-container {
                    height: auto;
                    min-height: 400px;
                }
                .canvas-node {
                    position: relative !important;
                    left: 0 !important;
                    top: 0 !important;
                    margin: 1rem 0;
                    max-width: none;
                }
                .canvas-edge {
                    display: none;
                }
            }
        </style>
<div class="canvas-node" id="node-d496a4076ca8b6f2" style="left: -206px; top: -153px;">
<div class="canvas-node-text">Test Canvas</div>
</div>
<div class="canvas-node" id="node-ecd6036b38b97a2b" style="left: -281px; top: -60px;">
<div class="canvas-node-file">
<a href="/blog/test-blog-2">Test Blog 2</a>
</div>
</div>
<div class="canvas-node" id="node-eeebaba9464d388d" style="left: 161px; top: -125px;">
<div class="canvas-node-file">
<a href="/blog/files/IMG-20250210021231508.pdf" target="_blank">IMG-20250210021231508.pdf</a>
</div>
</div>
<div class="canvas-node" id="node-fe7b5889183c6889" style="left: 161px; top: 320px;">
<div class="canvas-node-file">
<img src="/blog/images/IMG-20250210021231096.jpeg" alt="IMG-20250210021231096.jpeg">
</div>
</div>
</div>
## Kanban - h2

<div class="kanban-board">
<style>
            .kanban-board {
                display: flex;
                gap: 1rem;
                overflow-x: auto;
                padding: 1rem 0;
                min-height: 400px;
                margin: 1rem 0;
                background: var(--background);
            }
            .kanban-lane {
                min-width: 300px;
                flex: 1;
                background: var(--background);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 1rem;
                display: flex;
                flex-direction: column;
            }
            .kanban-lane-header {
                font-weight: bold;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid var(--accent);
                color: var(--color);
            }
            .kanban-cards {
                flex: 1;
                min-height: 100px;
            }
            .kanban-card {
                background: var(--background);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 0.75rem;
                margin-bottom: 0.75rem;
                transition: transform 0.2s;
            }
            .kanban-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .kanban-card-text {
                color: var(--color);
                font-size: 0.9rem;
                white-space: pre-wrap;
            }
            .kanban-card-checkbox {
                margin-right: 0.5rem;
                opacity: 0.6;
            }
            .kanban-card-title {
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            .kanban-card-checklist {
                margin-left: 1.5rem;
                margin-top: 0.5rem;
            }
            .kanban-card-checklist-item {
                display: flex;
                align-items: flex-start;
                margin-bottom: 0.25rem;
            }
            @media (max-width: 768px) {
                .kanban-board {
                    flex-direction: column;
                }
                .kanban-lane {
                    min-width: 100%;
                }
            }
        </style>
<div class="kanban-lane">
<div class="kanban-lane-header">1</div>
<div class="kanban-cards">
<div class="kanban-card">
<div class="kanban-card-title">First Card</div>
</div>
</div>
</div>
<div class="kanban-lane">
<div class="kanban-lane-header">2</div>
<div class="kanban-cards">
<div class="kanban-card">
<div class="kanban-card-text"><span class="kanban-card-checkbox">☐</span>Another One</div>
</div>
<div class="kanban-card">
<div class="kanban-card-text"><span class="kanban-card-checkbox">☐</span>Checklist</div>
</div>
</div>
</div>
<div class="kanban-lane">
<div class="kanban-lane-header">3</div>
<div class="kanban-cards">
<div class="kanban-card">
<div class="kanban-card-text"><span class="kanban-card-checkbox">☐</span>Test</div>
</div>
</div>
</div>
</div>