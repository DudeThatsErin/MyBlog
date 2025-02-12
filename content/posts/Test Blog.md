---
title: My Test Blog Post
date: 2024-02-10
author: Erin
description: This is a test blog post about software engineering
tags:
  - software
  - engineering
  - tutorial
categories:
  - tech
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
                color: var(--accent);
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
                color: var(--foreground);
                font-size: 0.9rem;
                white-space: pre-wrap;
            }
            .kanban-card-title {
                font-weight: bold;
                margin-bottom: 0.5rem;
                color: var(--accent);
            }
            .kanban-card-checklist {
                margin-top: 0.5rem;
                list-style: none;
                padding-left: 0;
            }
            .kanban-card-checklist-item {
                display: flex;
                align-items: flex-start;
                margin-bottom: 0.25rem;
                color: var(--foreground);
            }
            .kanban-card-checkbox {
                margin-right: 0.5rem;
                opacity: 0.6;
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
<div class="kanban-card-text">Text</div>
</div>
</div>
</div>
<div class="kanban-lane">
<div class="kanban-lane-header">2</div>
<div class="kanban-cards">
<div class="kanban-card">
<div class="kanban-card-text">Another One</div>
<ul class="kanban-card-checklist">
<li class="kanban-card-checklist-item">
<span class="kanban-card-checkbox">☐</span>Checklist
</li>
</ul>
</div>
</div>
</div>
<div class="kanban-lane">
<div class="kanban-lane-header">3</div>
<div class="kanban-cards">
<div class="kanban-card">
<div class="kanban-card-text">Test</div>
<div class="kanban-card-text">%% kanban:settings<br>```<br>{"kanban-plugin":"board","list-collapse":[false,false,false]}<br>```<br>%%</div>
</div>
</div>
</div>
</div>