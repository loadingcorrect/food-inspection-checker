// 页码点击跳转功能
// 使用事件委托机制,避免重复绑定事件处理器

document.addEventListener('DOMContentLoaded', function () {
    // 使用事件委托:在 document 上监听所有点击事件
    document.addEventListener('click', function (e) {
        // 查找被点击的元素或其父元素是否是页码标签
        const badge = e.target.closest('.page-badge, [data-page]');

        if (badge && badge.hasAttribute('data-page')) {
            const page = badge.getAttribute('data-page');

            if (page && typeof switchPdfView === 'function') {
                // 跳转到细则对应页面
                switchPdfView('rules', parseInt(page));

                // 视觉反馈:点击效果
                const originalBg = badge.style.background;
                badge.style.background = '#1d4ed8';
                setTimeout(() => {
                    badge.style.background = originalBg || '#3b82f6';
                }, 300);
            }
        }
    });

    // 初始化样式:为所有页码标签添加基础样式和悬停效果
    function initPageBadgeStyles() {
        const pageBadges = document.querySelectorAll('.page-badge, [data-page]');

        pageBadges.forEach(badge => {
            const page = badge.getAttribute('data-page');

            if (page && !badge.getAttribute('data-styled')) {
                // 标记已初始化样式
                badge.setAttribute('data-styled', 'true');

                // 基础样式
                badge.style.cursor = 'pointer';
                badge.style.transition = 'all 0.2s';
                badge.title = `点击跳转到细则第 ${page} 页`;

                // 鼠标悬停效果
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
            }
        });
    }

    // 初始化
    initPageBadgeStyles();

    // 监听内容变化,为新添加的页码标签初始化样式
    const observer = new MutationObserver(function (mutations) {
        initPageBadgeStyles();
    });

    const mainContent = document.querySelector('.main-content') || document.body;
    observer.observe(mainContent, {
        childList: true,
        subtree: true
    });
});
