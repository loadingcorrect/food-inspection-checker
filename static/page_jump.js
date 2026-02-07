// 页码点击跳转功能
// 在页面加载完成后,为所有页码标签添加点击事件

document.addEventListener('DOMContentLoaded', function () {
    // 为所有页码标签添加点击事件
    function addPageClickHandlers() {
        const pageBadges = document.querySelectorAll('.page-badge, [data-page]');

        pageBadges.forEach(badge => {
            const page = badge.getAttribute('data-page');
            if (page) {
                // 添加点击事件
                badge.addEventListener('click', function () {
                    // 调用 switchPdfView 函数跳转到细则对应页面
                    if (typeof switchPdfView === 'function') {
                        switchPdfView('rules', parseInt(page));
                        // 视觉反馈
                        this.style.background = '#1d4ed8';
                        setTimeout(() => {
                            this.style.background = '#3b82f6';
                        }, 300);
                    } else {
                        console.error('switchPdfView function not found');
                    }
                });

                // 添加悬停效果
                badge.addEventListener('mouseenter', function () {
                    this.style.background = '#2563eb';
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 4px 6px rgba(59,130,246,0.3)';
                });

                badge.addEventListener('mouseleave', function () {
                    this.style.background = '#3b82f6';
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = 'none';
                });

                // 添加样式
                badge.style.cursor = 'pointer';
                badge.style.transition = 'all 0.2s';
                badge.title = `点击跳转到细则第 ${page} 页`;
            }
        });
    }

    // 初始添加
    addPageClickHandlers();

    // 监听内容变化,重新添加事件处理器
    const observer = new MutationObserver(function (mutations) {
        addPageClickHandlers();
    });

    // 观察主内容区域的变化
    const mainContent = document.querySelector('.main-content') || document.body;
    observer.observe(mainContent, {
        childList: true,
        subtree: true
    });
});
