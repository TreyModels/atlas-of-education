(function () {
  if (typeof MutationObserver === 'undefined' || !document.createTreeWalker) return;
  const lang = new URLSearchParams(location.search).get('lang');
  if (lang !== 'zh-Hans' && lang !== 'vi') return;
  const labels = /*LOCALES*/;
  const column = lang === 'zh-Hans' ? 0 : 1;
  const zh = column === 0;
  document.documentElement.lang = lang;

  function translate(value) {
    const key = value.trim().replace(/\s+/g, ' ');
    if (Object.hasOwn(labels, key)) return value.replace(value.trim(), labels[key][column]);
    const sentence = key.match(/^(.+?)\. (.+)$/);
    if (sentence && Object.hasOwn(labels, sentence[1]) && Object.hasOwn(labels, sentence[2])) {
      return labels[sentence[1]][column] + (zh ? '。' : '. ') + labels[sentence[2]][column];
    }
    const tooltip = key.match(/^(.+) · ([\d,.–—]+)$/);
    if (tooltip && Object.hasOwn(labels, tooltip[1])) return labels[tooltip[1]][column] + ' · ' + tooltip[2];
    const dated = key.match(/^(.+) in (\d{4}(?:\/\d{2})?)$/);
    if (dated && Object.hasOwn(labels, dated[1])) {
      const label = labels[dated[1]][column];
      return zh ? dated[2] + '年 ' + label : label + ' năm ' + dated[2];
    }
    const p1 = key.match(/^(\d{4}\/\d{2}) modeled P1$/);
    if (p1) return zh ? p1[1] + ' 模拟小一' : 'Lớp 1 mô phỏng ' + p1[1];
    const chart = key.match(/^(.+) (from 2025 through 2050|by year under three policies)$/);
    if (chart && Object.hasOwn(labels, chart[1])) {
      const suffix = chart[2].startsWith('from')
        ? (zh ? '，2025至2050年' : ' từ 2025 đến 2050')
        : (zh ? '，三种政策的逐年结果' : ' theo năm dưới ba chính sách');
      return labels[chart[1]][column] + suffix;
    }
    const error = key.match(/^Retrospective one-year enrollment check \((\d+) years?\)\. Age-based scaling had (.+?)% weighted error, compared with (.+?)% holding enrollment flat\. The UN age series is from a single release, including projections for 2024 onward\.$/);
    if (error) return zh
      ? `入学人数的一年期回测（${error[1]}年）。按年龄组推算的加权误差为${error[2]}%，维持入学人数不变的误差为${error[3]}%。联合国年龄序列来自同一发布版本，包括2024年起的预测。`
      : `Kiểm định hồi cứu dự báo số học sinh một năm (${error[1]} năm). Sai số có trọng số theo độ tuổi là ${error[2]}%, so với ${error[3]}% khi giữ nguyên số học sinh. Chuỗi Liên Hợp Quốc lấy từ một lần công bố, gồm dự báo từ 2024.`;
    const test = key.match(/^(.+) · (schools MAE|WAPE)$/);
    if (test && Object.hasOwn(labels, test[1])) return labels[test[1]][column] + ' · ' + (test[2] === 'WAPE' ? 'WAPE' : zh ? '学校数平均绝对误差' : 'MAE số trường');
    const bulletin = key.match(/^(\d{4}) bulletin$/);
    if (bulletin) return zh ? bulletin[1] + '年公报' : 'Bản tin năm ' + bulletin[1];
    const birthIndex = key.match(/^(\d+) · ([\d,]+) births$/);
    if (birthIndex) return zh ? `${birthIndex[1]} · ${birthIndex[2]}人出生` : `${birthIndex[1]} · ${birthIndex[2]} ca sinh`;
    const playing = key.match(/^Playing completed run · (.+)$/);
    if (playing) return zh ? `正在播放已完成的运行 · ${playing[1]}` : `Đang phát kết quả đã tính · ${playing[1]}`;
    const paused = key.match(/^Paused · (.+)$/);
    if (paused) return zh ? `已暂停 · ${paused[1]}` : `Đã tạm dừng · ${paused[1]}`;
    const ready = key.match(/^Completed run ready · inspecting (.+)$/);
    if (ready) return zh ? `已完成的运行已就绪 · 正在查看${ready[1]}` : `Kết quả sẵn sàng · đang xem ${ready[1]}`;
    return value;
  }

  function translateText(node) {
    const parent = node.parentElement;
    if (!parent || parent.closest('script,style')) return;
    const translated = translate(node.nodeValue);
    if (translated !== node.nodeValue) {
      if (parent.tagName === 'OPTION' && !parent.hasAttribute('value')) parent.value = parent.text;
      node.nodeValue = translated;
    }
  }

  function translateElement(element) {
    for (const name of ['aria-label', 'title', 'placeholder']) {
      if (!element.hasAttribute(name)) continue;
      const value = element.getAttribute(name);
      const translated = translate(value);
      if (translated !== value) element.setAttribute(name, translated);
    }
  }

  function translateTree(root) {
    if (root.nodeType === Node.TEXT_NODE) {
      translateText(root);
      return;
    }
    if (root.nodeType !== Node.ELEMENT_NODE || root.matches('script,style')) return;
    translateElement(root);
    const tree = document.createTreeWalker(root, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
    for (let node = tree.nextNode(); node; node = tree.nextNode()) {
      if (node.nodeType === Node.TEXT_NODE) translateText(node);
      else translateElement(node);
    }
  }

  translateTree(document.documentElement);
  new MutationObserver(records => {
    for (const record of records) {
      if (record.type === 'attributes') translateElement(record.target);
      else if (record.type === 'characterData') translateText(record.target);
      else record.addedNodes.forEach(translateTree);
    }
  }).observe(document.documentElement, {
    subtree: true, childList: true, characterData: true, attributes: true,
    attributeFilter: ['aria-label', 'title', 'placeholder'],
  });
})();
