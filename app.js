'use strict';

const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
const mobileMenu = matchMedia('(max-width: 760px)');
function closeMenu(restoreFocus = false) {
  menuButton?.setAttribute('aria-expanded', 'false');
  navigation?.classList.remove('open');
  if (restoreFocus) menuButton?.focus();
}
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('open', open);
});
mobileMenu.addEventListener('change', () => closeMenu());
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && navigation?.classList.contains('open')) closeMenu(true);
});
document.addEventListener('click', event => {
  if (!event.target.closest('header')) closeMenu();
});
document.addEventListener('focusin', event => {
  if (!event.target.closest('header')) closeMenu();
});
navigation?.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});

const filters = document.querySelectorAll('[data-filter]');
filters.forEach(button => button.addEventListener('click', () => {
  filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  document.querySelectorAll('.portfolio-item').forEach(item => {
    item.hidden = button.dataset.filter !== 'All' && item.dataset.category !== button.dataset.filter;
  });
}));

const dialog = document.querySelector('#gallery');
let galleryTrigger;
document.querySelectorAll('[data-image]').forEach(button => button.addEventListener('click', () => {
  galleryTrigger = button;
  const image = dialog.querySelector('img');
  image.src = '/assets/' + button.dataset.image + '.webp';
  image.alt = button.dataset.title + ' — SOCOR archive';
  dialog.querySelector('p').textContent = button.dataset.title;
  dialog.showModal();
}));
dialog?.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog?.addEventListener('click', event => {
  const bounds = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
});
dialog?.addEventListener('close', () => galleryTrigger?.focus());

const equipmentSearch = document.querySelector('#equipment-search');
equipmentSearch?.addEventListener('input', () => {
  let count = 0;
  const query = equipmentSearch.value.trim().toLowerCase();
  document.querySelectorAll('tbody tr').forEach(row => {
    row.hidden = !row.cells[0].textContent.toLowerCase().includes(query);
    if (!row.hidden) count++;
  });
  document.querySelector('#equipment-count').textContent = count + ' equipment types';
  document.querySelector('#no-equipment').hidden = count !== 0;
});

// A separate origin has no verified WordPress submission integration. Never
// present an unverified request as delivered. Retain the user's text locally
// in the form and prepare an explicit email handoff; no request is sent here.
const form = document.querySelector('#inquiry');
if (form) {
  const status = document.querySelector('#form-status');
  const emailDraft = document.querySelector('#email-draft');
  const selected = new URLSearchParams(location.search).get('service');
  const allowedServices = ['hot-mix-asphalt', 'ready-mix-concrete', 'aggregates', 'equipment-rental', 'land-transport'];
  if (allowedServices.includes(selected)) {
    form.querySelector('textarea').value = 'I would like to inquire about ' + selected.replaceAll('-', ' ') + '.\n';
  }
  form.addEventListener('input', () => {
    emailDraft.hidden = true;
    emailDraft.removeAttribute('href');
    status.textContent = '';
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const value = name => form.elements.namedItem('form_fields[' + name + ']').value.trim();
    const fullName = value('name') + ' ' + value('field_fccabf3');
    const body = 'Name: ' + fullName + '\nEmail: ' + value('email') + '\nPhone: ' + value('field_ff3133b') + '\n\nProject inquiry:\n' + value('message');
    const url = 'mailto:socorcebu@socorconstruction.com?subject=' + encodeURIComponent('Project inquiry — ' + fullName) + '&body=' + encodeURIComponent(body);
    if (url.length > 7000) {
      status.textContent = 'This inquiry is too long for a reliable email handoff. Please shorten the project description or email SOCOR directly. Your details are retained.';
      emailDraft.hidden = true;
      return;
    }
    emailDraft.href = url;
    emailDraft.hidden = false;
    status.textContent = 'Your email is ready to open. Nothing has been sent. Open it below, then review and send it in your email app.';
  });
}

const siteHeader = document.querySelector('header');
function updateHeader() { siteHeader?.classList.toggle('scrolled', scrollY > 160); }
addEventListener('scroll', updateHeader, { passive: true });
addEventListener('pageshow', updateHeader);

// Content is visible by default. Enhance only when motion is welcome and a
// photograph enters the viewport; never delay reading or keyboard navigation.
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
if (!reducedMotion.matches && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-once');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('main figure img, .service-editorials img, .editorial-image img').forEach(image => observer.observe(image));
  reducedMotion.addEventListener('change', event => {
    if (event.matches) {
      observer.disconnect();
      document.querySelectorAll('.reveal-once').forEach(image => image.classList.remove('reveal-once'));
    }
  });
}
