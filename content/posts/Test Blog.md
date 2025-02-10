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
            }
            .canvas-node {
                position: absolute;
                background: var(--background);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 1rem;
                max-width: 300px;
            }
            .canvas-node-text {
                font-size: 0.9rem;
            }
            .canvas-edge {
                position: absolute;
                border-top: 2px solid var(--accent);
                opacity: 0.5;
            }
            @media (max-width: 768px) {
                .canvas-container {
                    height: auto;
                    min-height: 400px;
                }
            }
        
</style>
<div class="canvas-node" style="left: -206px; top: -153px;">
<div class="canvas-node-text">Test Canvas</div>
</div>
<div class="canvas-node" style="left: -281px; top: -60px;">
<div class="canvas-node-text"></div>
</div>
<div class="canvas-node" style="left: 161px; top: -125px;">
<div class="canvas-node-text"></div>
</div>
<div class="canvas-node" style="left: 161px; top: 320px;">
<div class="canvas-node-text"></div>
</div>
</div>
## Kanban - h2
![[Untitled Kanban|embed]]