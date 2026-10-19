<?php
// Center SIM — campanha "Sua compra vale mais": poe o banner como 1o slide da home (pagina 3207).
// Uso: wp eval-file golive.php [dry]   (idempotente; backup do _elementor_data antes de gravar)
$dry = in_array('dry', $args ?? [], true);
$pid = 3207;
$slide = file_get_contents(__DIR__ . '/slide.html');
$dot = '<!-- campanha-suacompravalemais:dot --><button aria-label="Slide campanha" class="hero-dot active" data-slide="campanha"></button>';
$raw = get_post_meta($pid, '_elementor_data', true);
$data = json_decode($raw, true);
$html = $data[0]['elements'][0]['settings']['html'];
if (strpos($html, 'campanha-suacompravalemais:slide-inicio') !== false) { echo "ja esta no ar\n"; return; }
file_put_contents(__DIR__ . '/backup-3207-' . date('Ymd-His') . '.json', $raw);
$n = 0;
$html = str_replace('<div class="hero-slides" id="hero-slides" style="transform: translateX(0%);">',
    '<div class="hero-slides" id="hero-slides" style="transform: translateX(0%);">' . "\n" . $slide, $html, $n1); $n += $n1;
// so o slide da campanha carrega com prioridade
$html = str_replace('decoding="async" fetchpriority="high" loading="eager" src="https://centersim.com.br/wp-content/uploads/2026/04/hero_1.png"',
    'decoding="async" loading="lazy" src="https://centersim.com.br/wp-content/uploads/2026/04/hero_1.png"', $html, $n2); $n += $n2;
$html = str_replace('<div class="hero-dots" id="hero-dots">' . "\n" . '<button aria-label="Slide 1" class="hero-dot active" data-slide="0"></button>',
    '<div class="hero-dots" id="hero-dots">' . "\n" . $dot . "\n" . '<button aria-label="Slide 1" class="hero-dot" data-slide="0"></button>', $html, $n3); $n += $n3;
echo "trocas: slide=$n1 hero1=$n2 dot=$n3\n";
if ($n1 !== 1 || $n3 !== 1) { echo "ABORTADO: marcacao da home mudou\n"; return; }
if ($dry) { echo "dry-run ok\n"; return; }
$data[0]['elements'][0]['settings']['html'] = $html;
update_post_meta($pid, '_elementor_data', wp_slash(wp_json_encode($data)));
delete_post_meta($pid, '_elementor_element_cache');
clean_post_cache($pid);
echo "NO AR\n";
