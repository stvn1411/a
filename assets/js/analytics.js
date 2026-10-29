/*
  Site-wide analytics (Google Analytics 4). Every page loads this one file, so the ID lives only here.
  GA4 records a page_view for each URL automatically: see per-page traffic in
  GA4 > Reports > Engagement > Pages and screens.

  Also sends:
  - affiliate_click: any link with rel="sponsored" (official-site buttons), with the product and page.
  - outbound_click is GA4's built-in "Outbound clicks" (Enhanced measurement), so it is not duplicated here.
*/
(function () {
  var GA_MEASUREMENT_ID = 'G-TYCDYV0LQ1'; // e.g. 'G-ABC123XYZ' from GA4 > Admin > Data streams

  // Don't load until an ID is set, and don't count local previews.
  var host = location.hostname;
  if (!GA_MEASUREMENT_ID || location.protocol === 'file:' || host === 'localhost' || host === '127.0.0.1') return;

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_MEASUREMENT_ID;
  document.head.appendChild(s);

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA_MEASUREMENT_ID);

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[rel~="sponsored"]');
    if (!a) return;
    gtag('event', 'affiliate_click', {
      product: a.getAttribute('data-product') || '',
      link_url: a.href,
      page_path: location.pathname,
      transport_type: 'beacon'
    });
  });
})();
