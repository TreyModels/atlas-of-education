'use strict';

(async function () {
  const axes = ['map-rows', 'map-columns', 'map-outcome'].map(id => document.getElementById(id));
  const grid = document.getElementById('map-grid');
  const legend = document.getElementById('map-legend');
  const detail = document.getElementById('map-detail');
  const names = [
    ['Share of early advantages that fades', '早期优势消退参数'],
    ['Home learning advantage', '家庭学习优势'],
    ['Neighborhood teacher advantage', '社区教师优势'],
    ['Early tutoring gain', '早期补习收益'],
    ['Wealth gap in enforcement', '不同家庭的政策执行差距'],
    ['Richer-to-poorer admission ratio at comparable ability', '同等能力下富裕组与较贫困组录取率之比'],
    ['Admission rate for poorer high-ability pupils', '较贫困高能力学生的录取率'],
  ];
  const language = () => document.documentElement.lang.startsWith('zh') ? 1 : 0;
  const labels = () => names.map(pair => pair[language()]);
  const el = (tag, value) => {
    const element = document.createElement(tag);
    if (value !== undefined) element.textContent = value;
    return element;
  };

  try {
    const response = await fetch('parameter-sweep.json');
    if (!response.ok) throw new Error('Sweep results unavailable');
    const {rows} = await response.json();
    const ranges = names.slice(0, 5).map((_, i) => {
      const column = rows.map(row => row[i]);
      return [Math.min(...column), Math.max(...column)];
    });
    const select = (control, items, selected) => {
      control.replaceChildren(...items.map(i => {
        const option = el('option', labels()[i]);
        option.value = i;
        return option;
      }));
      control.value = selected;
    };
    const valueText = (value, outcome) => outcome === 6
      ? (100 * value).toFixed(1) + '%' : value.toFixed(2) + '×';
    const limit = (axis, band) => {
      const [min, max] = ranges[axis];
      return (min + (max - min) * band / 4).toFixed(3);
    };
    const bin = (value, [min,max]) => Math.min(3, Math.floor(4 * (value - min) / (max - min)));

    function render() {
      const zh = language() === 1;
      const [rowAxis, colAxis, outcome] = axes.map(a => Number(a.value));
      const cells = Array.from({length: 16}, () => ({sum: 0, n: 0}));
      for (const row of rows) {
        const cell = cells[4 * bin(row[rowAxis],ranges[rowAxis]) + bin(row[colAxis],ranges[colAxis])];
        cell.n++;
        cell.sum += row[outcome];
      }
      const values = cells.filter(c => c.n > 0).map(c => c.sum / c.n);
      const min = Math.min(...values), max = Math.max(...values);
      const explain = outcome === 5 ? (zh ? '1× 表示两组的录取率相同。' : 'At 1× both groups have the same admission rate.')
        : (zh ? '较贫困组指本地家庭财富最低 40%，高能力指初始能力前 10%。'
          : 'Poorer means the bottom 40% of locally registered households. High ability means the top tenth in starting ability.');
      legend.textContent = (zh ? '浅色 ' : 'Lighter ') + valueText(min,outcome) + ' · ' +
        (zh ? '深色 ' : 'Darker ') + valueText(max,outcome) + '. ' + explain;
      detail.textContent = zh ? '选择方格可查看区间和样本数。' : 'Select a square to see the exact ranges and run count.';
      const table = el('tbody');
      const header = el('tr');
      header.append(el('td'));
      for (let x = 0; x < 4; x++) {
        const th = el('th', String(x+1)); th.scope = 'col'; header.append(th);
      }
      const thead = el('thead');
      thead.append(header);
      for (let y = 0; y < 4; y++) {
        const tr = el('tr'), th = el('th', String(y+1)); th.scope = 'row'; tr.append(th);
        for (let x = 0; x < 4; x++) {
          const td = el('td'), cell = cells[y * 4 + x];
          const value = cell.sum / cell.n;
          const btn = el('button', cell.n ? valueText(value,outcome) : '—');
          btn.type = 'button';
          const intensity = cell.n ? (value-min)/(max-min || 1) : 0;
          if (cell.n) {
            btn.style.backgroundColor = 'hsl(169 43% ' + (94-65*intensity) + '%)';
            btn.style.color = intensity >= .60 ? '#fff' : '#102f35';
          }
          const description = labels()[rowAxis] + ' ' + limit(rowAxis,y) + '–' + limit(rowAxis,y+1) + ' · ' +
            labels()[colAxis] + ' ' + limit(colAxis,x) + '–' + limit(colAxis,x+1) + ' · ' +
            (cell.n ? valueText(value,outcome) + ' (' + cell.n + (zh ? ' 组设定)' : ' saved settings)') : (zh ? '无取样' : 'No saved settings'));
          btn.setAttribute('aria-label', description);
          btn.addEventListener('click', () => {
            grid.querySelector('[aria-pressed="true"]')?.setAttribute('aria-pressed', 'false');
            btn.setAttribute('aria-pressed', 'true');
            detail.textContent = description;
          });
          btn.setAttribute('aria-pressed', 'false');
          td.append(btn); tr.append(td);
        }
        table.append(tr);
      }
      grid.replaceChildren(thead,table);
    }

    function populate(row = 0, col = 1, outcome = 5) {
      select(axes[0],[0,1,2,3,4],row);
      select(axes[1],[0,1,2,3,4].filter(i => i !== row),row === col ? (row === 0 ? 1 : 0) : col);
      select(axes[2],[5,6],outcome);
      render();
    }
    axes[0].addEventListener('change', () => populate(...axes.map(a => Number(a.value))));
    axes.slice(1).forEach(a => a.addEventListener('change',render));
    new MutationObserver(() => populate(...axes.map(a => Number(a.value))))
      .observe(document.documentElement,{attributes: true,attributeFilter:['lang']});
    populate();
  } catch (error) {
    detail.textContent = language() ? '无法加载已保存的参数扫描结果。' : 'The saved sweep could not be loaded.';
    console.error(error);
  }
})();
