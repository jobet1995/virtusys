(function ($, window, document) {
  "use strict";

  class ExceptionHandler {
    static handle(error, context = 'Global') {
      console.error(`[VirtuSys Error] [${context}]`, error);
      if (window.bootstrap && typeof bootstrap.Toast !== 'undefined') {
        const toast = `
          <div class="toast align-items-center text-bg-danger border-0 position-fixed bottom-0 end-0 m-3" role="alert">
            <div class="d-flex">
              <div class="toast-body">An unexpected error occurred. Please try again later.</div>
              <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
          </div>`;
        $('body').append(toast);
        const toastEl = document.querySelector('.toast:last-child');
        new bootstrap.Toast(toastEl).show();
      }
    }
  }

  class AjaxService {
    static request({ url, method = 'GET', data = {}, onSuccess, onError }) {
      $.ajax({
        url,
        method,
        data,
        dataType: 'json',
        async: true,
        cache: false,
      })
        .done((response) => {
          if (typeof onSuccess === 'function') onSuccess(response);
        })
        .fail((xhr, status, error) => {
          const errObj = { status, error, responseText: xhr.responseText };
          ExceptionHandler.handle(errObj, `AJAX ${method} ${url}`);
          if (typeof onError === 'function') onError(errObj);
        });
    }
  }

  class UIController {
    static init() {
      this.registerEvents();
      this.smoothScroll();
      this.handleResponsiveState();
      this.initAnimations();
    }

    static registerEvents() {
      $(window).on('load', () => this.onPageLoad());
      $(window).on('scroll', () => this.onScroll());
      $(window).on('resize', () => this.onResize());
    }

    static onPageLoad() {
      AjaxService.request({
        url: '/api/v2/pages/?type=blog.BlogPage&fields=title,intro',
        onSuccess: (data) => this.updateContent('#blog-list', data),
      });
      
      // Trigger animation for elements already in view
      this.animateOnScroll();
    }

    static onScroll() {
      const scrollTop = $(window).scrollTop();
      if (scrollTop > 100) $('.navbar').addClass('scrolled');
      else $('.navbar').removeClass('scrolled');
      
      // Check for elements to animate
      this.animateOnScroll();
    }

    static onResize() {
      this.handleResponsiveState();
    }

    static smoothScroll() {
      $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();
        const target = $($(this).attr('href'));
        if (target.length) {
          $('html, body').animate({ scrollTop: target.offset().top }, 600);
        }
      });
    }

    static handleResponsiveState() {
      const width = $(window).width();
      window.isMobile = width < 768;
    }

    static updateContent(containerSelector, data) {
      if (!data || !data.items) return;
      const container = $(containerSelector);
      const items = data.items.map((item) => `<li>${item.title}</li>`).join('');
      container.html(`<ul>${items}</ul>`);
    }
    
    // Initialize animations for elements with slide-up class
    static initAnimations() {
      // Add transition for slide-up elements
      $('.slide-up').each(function() {
        const $element = $(this);
        // Check if element is already in view
        if (this.getBoundingClientRect().top < window.innerHeight - 100) {
          $element.addClass('visible');
        }
      });
    }
    
    // Animate elements when they come into view
    static animateOnScroll() {
      $('.slide-up:not(.visible)').each(function() {
        const $element = $(this);
        const elementTop = this.getBoundingClientRect().top;
        const elementBottom = elementTop + this.offsetHeight;
        const viewportHeight = window.innerHeight;
        
        // If element is in viewport (with some buffer)
        if (elementTop < viewportHeight - 100 && elementBottom > 0) {
          $element.addClass('visible');
        }
      });
    }
  }

  window.VirtuSysGlobal = {
    AjaxService,
    UIController,
    ExceptionHandler,
  };

  $(document).ready(() => {
    try {
      UIController.init();
    } catch (err) {
      ExceptionHandler.handle(err, 'Initialization');
    }
  });

})(jQuery, window, document);