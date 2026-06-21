(function () {
  const page = location.pathname.split('/').pop() || 'index.html';
  const NAV = [
    { href: '/',              label: 'Ratings'   },
    { href: 'breakdown.html', label: 'Breakdown' },
    { href: 'about.html',     label: 'About'     },
  ];
  const links = NAV.map(({ href, label }) => {
    const current = (href === '/' ? 'index.html' : href) === page ? ' aria-current="page"' : '';
    return `<a href="${href}" class="nav-link"${current}>${label}</a>`;
  }).join('\n      ');

  document.currentScript.insertAdjacentHTML('beforebegin',
    `<header class="site-header">
    <div class="site-header-main">
      <img class="site-logo" src="logo.jpg" alt="Biff! podcast logo">
      <div>
        <h1>Biff! Ratings</h1>
        <p class="tagline">In which we take a silly rating system very seriously.</p>
      </div>
    </div>
    <nav class="site-nav">
      ${links}
    </nav>
  </header>`
  );
}());
