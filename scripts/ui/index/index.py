def _custom_css():
        return """
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@500&display=swap');

        html.theme-dark body {
            background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
            color: white;
        }

        html.theme-dark .typing-title {
            color: white;
        }

        /* Light theme */
        html.theme-light body {
            background: linear-gradient(to bottom, #ffffff, #f7f7f7, #e0e0e0);
            color: black;
        }

        html.theme-light .typing-title {
            color: black;
        }

        body {
            font-family: 'Roboto Mono', monospace;
        }

        .typing-title {
            display: inline-block;
            font-size: 2rem;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
            white-space: nowrap;
            overflow: hidden;
            border-right: 0.15em solid white;
            animation: typing 3s steps(40, end), blink-caret 0.75s step-end infinite;
            max-width: 100%;
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }

        @keyframes blink-caret {
            50% { border-color: transparent }
        }

        .card-container {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin-top: 2rem;
            flex-wrap: wrap;
        }

        .card {
            background: rgba(220,220,220, 0.3);
            box-shadow: 0 0 10px rgba(220,220,220, 0.3);
            border-radius: 12px;
            padding: 1.5rem;
            width: 250px;
            text-align: center;
            transition: transform 0.3s;
        }

        .card:hover {
            transform: scale(1.05);
            background: rgba(220,220,220, 0.3);
        }

        .card-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .card-title {
            font-size: 1.3rem;
            margin-bottom: 0.3rem;
            font-weight: bold;
        }

        .additional-info {
            margin-top: 3rem;
            background: rgba(220,220,220, 0.3);
            padding: 2rem;
            border-radius: 12px;
            animation: fadeIn 1s ease-in;
        }

        .additional-info h2, .additional-info h3 {
            margin-top: 1.5rem;
            font-weight: 600;
        }

        .tech-list {
            list-style: none;
            padding-left: 0;
            margin-top: 1rem;
        }

        .tech-list li {
            margin: 0.5rem 0;
            text-align: left;
            padding-left: 2rem;
            position: relative;
        }

        .tech-list li::before {
            content: "✔️";
            position: absolute;
            left: 0;
            top: 0;
        }

        .badges {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
        }

        .badge {
            background: #ffffff22;
            padding: 0.3rem 0.8rem;
            border-radius: 6px;
            font-size: 0.9rem;
            backdrop-filter: blur(5px);
        }

        /* Particle background for animation */
        .particle-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }
        """

def _landing_html():
    return """
    <div style='text-align: center; margin-top: 60px; max-width: 1000px; margin-left: auto; margin-right: auto;'>
        <div style="width: 100%; text-align: center; margin-top: 60px;">
            <div class="typing-title">欢迎来到多语言本地化生成系统</div>
        </div>
        <p style='margin-top: 1rem;'>一个基于大语言模型、Gradio、LoRA 的翻译与微调平台</p>

        <div class="card-container">
            <div class="card">
                <div class="card-icon">🧠</div>
                <div class="card-title">微调训练</div>
                <p>快速接入 LoRA 微调，灵活调整训练流程</p>
            </div>
            <div class="card">
                <div class="card-icon">📊</div>
                <div class="card-title">翻译评估</div>
                <p>翻译质量可视化，支持多种评估算法对比分析，支持回译评估</p>
            </div>
            <div class="card">
                <div class="card-icon">📝</div>
                <div class="card-title">批量翻译</div>
                <p>针对Excel配表进行翻译操作，高效批量翻译</p>
            </div>
        </div>

        <div class='additional-info'>
            <h2 style="text-align:center;">系统简介</h2>
            <p style="text-align:center;">本系统融合大语言模型、UI 控制、模型管理与训练评估功能，为中小团队提供一站式多语言解决方案。</p>

            <h3 style="text-align:center;">核心特色</h3>
            <ul class="tech-list" style="text-align:center; display:inline-block;">
                <li>多语言目标支持（中文、英文、日语、德语...）</li>
                <li>模型格式自动识别与加载</li>
                <li>基于 LoRA 的高效训练流程与微调翻译</li>
                <li>训练阶段可视化分析与采样测试</li>
                <li>翻译准确度评估与回译评估</li>
                <li>批量翻译，配表操作</li>
            </ul>

            <h3 style="text-align:center;">开源组件</h3>
            <div class="badges" style="justify-content: center;">
                <span class="badge">Gradio</span>
                <span class="badge">Transformers</span>
                <span class="badge">LoRA</span>
                <span class="badge">GGUF</span>
                <span class="badge">FastAPI</span>
                <span class="badge">Tokenizers</span>
                <span class="badge">Matplotlib</span>
            </div>

            <h3 style="text-align:center;">项目背景</h3>
            <p style="text-align:center;">随着多语言应用的增长，中小开发团队亟需低成本、高效率的本地化解决方案。本项目基于 Transformer 模型结构，通过 LoRA 微调和自定义数据训练，大幅降低训练成本并提升生成质量。</p>

            <h3 style="text-align:center;">版本信息</h3>
            <p style="text-align:center;">Version 1.0.0 | Last updated: 2025-03-24</p>
        </div>
    </div>
    """