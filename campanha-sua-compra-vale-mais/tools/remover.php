<?php
// Center SIM — fim da campanha "Sua compra vale mais" (31/12/2026): tira o slide da home e
// troca a LP por um redirecionamento pra home (arquivo da LP fica em ~/campanhas/sua-compra-vale-mais/lp-arquivada).
$pid = 3207;
$raw = get_post_meta($pid, '_elementor_data', true);
$data = json_decode($raw, true);
$html = $data[0]['elements'][0]['settings']['html'];
if (strpos($html, 'campanha-suacompravalemais:slide-inicio') !== false) {
    file_put_contents(__DIR__ . '/backup-3207-remocao-' . date('Ymd-His') . '.json', $raw);
    $html = preg_replace('#\n?<!-- campanha-suacompravalemais:slide-inicio -->.*?<!-- campanha-suacompravalemais:slide-fim -->#s', '', $html);
    $html = preg_replace('#<!-- campanha-suacompravalemais:dot --><button[^>]*></button>\n?#', '', $html);
    $html = str_replace('<button aria-label="Slide 1" class="hero-dot" data-slide="0"></button>', '<button aria-label="Slide 1" class="hero-dot active" data-slide="0"></button>', $html);
    $html = str_replace('decoding="async" loading="lazy" src="https://centersim.com.br/wp-content/uploads/2026/04/hero_1.png"',
        'decoding="async" fetchpriority="high" loading="eager" src="https://centersim.com.br/wp-content/uploads/2026/04/hero_1.png"', $html);
    $data[0]['elements'][0]['settings']['html'] = $html;
    update_post_meta($pid, '_elementor_data', wp_slash(wp_json_encode($data)));
    delete_post_meta($pid, '_elementor_element_cache');
    clean_post_cache($pid);
    echo "slide removido\n";
} else { echo "slide ja nao estava\n"; }
$lp = ABSPATH . 'campanhasuacompravalemais';
$arq = __DIR__ . '/lp-arquivada';
if (is_dir($lp) && !is_dir($arq)) {
    rename($lp, $arq);
    mkdir($lp, 0755);
    file_put_contents($lp . '/index.php', "<?php header('Location: /', true, 302); exit;\n");
    echo "LP arquivada e redirecionando pra home\n";
}
