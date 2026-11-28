'use strict';

window.GZ_I18N = {
  en: {
    htmlLang: 'en',
    pageTitle: 'Guangzhou Education Explorer · Atlas of Education',
    brandTitle: 'Atlas of Education',
    githubRepo: 'GitHub Repository',
    kicker: 'INTERACTIVE RESEARCH COMPANION · REVISION 1.4',
    heroTitle: 'Educational Opportunity & Private Tutoring in Guangzhou',
    heroLead: 'Can a talented pupil from a low-income family reach a selective university through Guangzhou’s academic track? Explore every precomputed simulation result, trace how school rules and tutoring choices interact, and challenge any of the 134 documented model assumptions.',
    bylineAuthor: 'Dr. Trey Menefee',
    bylineMeta: 'Working paper companion · 28 November 2026',
    badgePrecomputed: 'Precomputed saved runs only',
    statPoor: 'Poorer 40% (local, top 10% ability)',
    statRich: 'Richer 40% (local, top 10% ability)',
    ratioLabel: 'Richer-to-poorer rate ratio:',
    ratioScore: 'by entrance score',
    ratioJoint: 'joint score & ability',
    ratioAbility: 'by starting ability',
    statNote: 'Medians across 1,024 settings (40,000 synthetic pupils each). Separate tutoring-choice runs use 40 settings across 8 matched seeds.',
    highlightsHeading: 'Key findings explained',
    highlightsSub: 'Select any finding to open its saved chart and compare parameter settings.',
    tabFindings: 'Explore results',
    tabAssumptions: 'Assumptions & tinker',
    tabSources: 'Sources, DOI & provenance',
    lblTopic: 'Research question',
    lblCase: 'Saved parameter setting',
    btnReset: 'Reset to baseline',
    btnCopyLink: 'Copy link to result',
    btnCopied: 'Link copied',
    guardrail: 'Controls step strictly through discrete saved runs from completed experiments. No live simulation is executed in the browser.',
    sweepHeading: 'Saved sweep overview',
    sweepSub: (n) => `${n} saved ${n === 1 ? 'case' : 'cases'} · click any row to jump`,
    casePos: (i, n) => `Case ${i} of ${n}`,
    deltaTitle: (label) => `Difference vs. baseline (${label}):`,
    assumpTitle: 'Assumptions, parameters & in-page tinkering',
    assumpLead: 'Inspect the default, tested range, and empirical basis for all 134 documented parameters across both models. Parameters marked Tinkerable include an inline saved-run slider so you can test how changing that assumption shifts the outcome—or flag any row with a structured critique.',
    lblSearch: 'Search parameters',
    phSearch: 'Try boarding, decay, income, hukou, or gain',
    lblGroup: 'Category',
    optAllGroups: 'All categories',
    lblModel: 'Model',
    optAllModels: 'Both models',
    lblTinkerableOnly: 'Show only parameters with saved interactive comparisons',
    assumpCount: (shown, total) => `Showing ${shown} of ${total} documented assumptions`,
    pillTinker: 'Tinkerable',
    metaModelCat: 'Model & category',
    metaDefault: 'Default value',
    metaRange: 'Saved range / uncertainty',
    basisPrefix: 'Evidence basis: ',
    inlineTinkerTitle: (label) => `In-page tinker · ${label}`,
    inlineSavedSetting: 'Saved setting:',
    vsBaseline: 'vs baseline',
    baselineTag: 'baseline',
    btnOpenChart: 'Open full chart',
    btnChallenge: 'Challenge / suggest adjustment',
    challengeTitle: (id) => `Challenge parameter: ${id}`,
    phSuggested: (val) => `Suggested value or range (current: ${val})`,
    phNote: 'Empirical source, Guangzhou context, or rationale for adjustment...',
    btnCopyNote: 'Copy structured note for James',
    noteCopied: 'Copied structured note to clipboard.',
    permalink: 'Permalink',
    srcTitle: 'Sources, citation & data provenance',
    srcLead: 'The principal admissions experiment spans 1,024 parameter settings with 40,000 synthetic pupils each. The revised tutoring-choice experiment spans 40 settings plus 2 legacy benchmarks across 8 paired 40,000-pupil cohorts (seeds 2201–2208). Both studies use synthetic cohorts to isolate mechanisms under stated assumptions.',
    citeHeading: 'Cite this working paper & collection',
    citeDoiLabel: 'Collection DOI:',
    btnCopyApa: 'Copy APA citation',
    btnCopyBib: 'Copy BibTeX',
    apaCopied: 'APA citation copied.',
    bibCopied: 'BibTeX copied.',
    dlHeading: 'Download verified data snapshots',
    dlData: 'All 14 topics & saved cases',
    dlAssump: 'Full 134-parameter register',
    dlProv: 'Experiment scope & SHA-256 hashes',
    dlGithub: 'GitHub working-paper archive (earlier revision)',
    dlZenodo: 'Zenodo Atlas of Education collection',
    anchorsHeading: 'Empirical & institutional anchors',
    provHeading: 'Cryptographic provenance (SHA-256)',
    provLead: 'Loaded live from provenance.json so every displayed chart can be traced directly back to its saved output file.',
    provColLayer: 'Layer',
    provColFile: 'File',
    provColHash: 'SHA-256',
    layerServed: 'Served snapshot',
    layerSource: 'Saved model output',
    footerLeft: 'Guangzhou Education Explorer · Revision 1.4 · Dr. Trey Menefee',
    footerRepo: 'Atlas source repository',
    loadError: 'The saved results could not be loaded. Refresh the page to try again.',
    storyCards: [
      {
        metric: '65.8% vs 81.8%',
        title: 'Open upward route with a persistent wealth gap',
        summary: 'In the top tenth of starting ability, about two-thirds of poorer local pupils reach a selective university proxy versus four-fifths of richer peers.',
        topic: 'access', caseIdx: 2
      },
      {
        metric: '0.91 → 1.17 → 1.37',
        title: 'Why the equity ratio flips by comparison',
        summary: 'At similar entrance scores, rates look near parity (0.91), because earlier family and school advantages are already baked into the exam score.',
        topic: 'fairness', caseIdx: 0
      },
      {
        metric: '58.2% → 70.4%',
        title: 'Early-advantage persistence is the largest lever',
        summary: 'Moving from low fade (≤15%) to high fade (75–90%) raises poorer high-ability access by 12.2 points—larger than any single tutoring shift.',
        topic: 'fade', caseIdx: 5
      },
      {
        metric: '0.08% → 24.7% term',
        title: 'Boarding compresses term tutoring into holidays',
        summary: 'Senior boarders buy almost no term tutoring at 1 h/week, yet 27.8% still buy in holidays. Expanding usable term time to 3 h/week unlocks term demand.',
        topic: 'calendar', caseId: 'board_longer_term'
      },
      {
        metric: '29.5% → 35.0%',
        title: 'Higher beliefs raise demand without higher gains',
        summary: 'Raising Grade 11 expected returns alone lifts annual participation by 5.5 points; raising realized learning gains alone leaves purchases unchanged.',
        topic: 'grade', caseId: 'g11_belief_only_039'
      },
      {
        metric: '3.0%–9.8% displaced · 0 premium',
        title: 'Rank displacement scales with tutoring efficacy',
        summary: 'Uniform restrictions add +0.25 pp centrally, while richer-family tutoring shifts 3.0%–9.8% down a rank band. ¥1.2M premium 1:1 attracts zero buyers.',
        topic: 'ranks', caseIdx: 3
      }
    ],
    topicGroups: {
      all: 'All questions (14)',
      core: 'Access & Equity',
      mech: 'Mechanisms & Restrictions',
      choice: 'Tutoring Choice & Timescapes',
      sens: 'Institutional & Skill Sensitivity'
    },
    models: {},
    groups: {},
    topics: {}
  },

  zh: {
    htmlLang: 'zh-Hans',
    pageTitle: '广州教育机会与校外补习交互浏览器 · 教育图谱 (Atlas of Education)',
    brandTitle: '教育图谱 · Atlas of Education',
    githubRepo: 'GitHub 代码与数据仓库',
    kicker: '交互式研究伴侣 · 修订版 1.4',
    heroTitle: '广州的教育机会与校外补习',
    heroLead: '一名家境普通但天资出众的学生，能否通过广州公办普通高中通道考入重点大学？本页面基于已保存的预计算模拟结果，支持交互探索升学规则与补习选择的机制，并公开全部 134 项模型假设供审阅与质疑。',
    bylineAuthor: 'Dr. Trey Menefee',
    bylineMeta: '工作论文交互伴侣 · 2026年11月28日',
    badgePrecomputed: '仅展示已保存预计算结果',
    statPoor: '收入后40%家庭（本地户籍、前10%能力）',
    statRich: '收入前40%家庭（本地户籍、前10%能力）',
    ratioLabel: '富贫重点大学通道比率：',
    ratioScore: '按中考分数比较',
    ratioJoint: '按分数与能力联合比较',
    ratioAbility: '按初始能力比较',
    statNote: '主实验 1,024 组设定的中位数（每组 40,000 名合成学生）；家庭补习选择扩展实验包含 40 组设定与 8 组配对随机种子。',
    highlightsHeading: '核心发现速览',
    highlightsSub: '点击任意卡片，直接跳转至对应的已保存图表与参数情境。',
    tabFindings: '探索模拟结果',
    tabAssumptions: '假设清单与页内调试',
    tabSources: '文献、DOI 与数据溯源',
    lblTopic: '研究问题',
    lblCase: '已保存参数情境',
    btnReset: '重置为基准设定',
    btnCopyLink: '复制当前结果链接',
    btnCopied: '链接已复制',
    guardrail: '所有滑块与下拉框严格切换已完成实验的离散保存结果，浏览器端不重新运行模拟，亦不插值生成未测试组合。',
    sweepHeading: '已保存情境全览',
    sweepSub: (n) => `共 ${n} 个已保存情境 · 点击任意行快速切换`,
    casePos: (i, n) => `第 ${i} / ${n} 个情境`,
    deltaTitle: (label) => `相对基准情境（${label}）的变化：`,
    assumpTitle: '全部 134 项模型假设、参数与页内调试',
    assumpLead: '查看两套模型中每项参数的默认值、测试区间与经验依据。标注「可交互调试」的参数内置预计算滑块，可直接观察调整该假设后结果如何变化；您也可对任意一条假设填写修正建议并一键复制结构化反馈。',
    lblSearch: '搜索参数或关键词',
    phSearch: '如：住校 (boarding)、消退 (decay)、收入 (income)、户籍 (hukou)',
    lblGroup: '参数类别',
    optAllGroups: '全部类别',
    lblModel: '所属模型',
    optAllModels: '全部模型',
    lblTinkerableOnly: '仅显示支持页内对比调试的参数',
    assumpCount: (shown, total) => `当前显示 ${shown} / ${total} 项已记录假设`,
    pillTinker: '可交互调试',
    metaModelCat: '模型与类别',
    metaDefault: '默认值',
    metaRange: '已测试区间 / 不确定性',
    basisPrefix: '依据来源：',
    inlineTinkerTitle: (label) => `页内调试 · ${label}`,
    inlineSavedSetting: '已保存设定：',
    vsBaseline: '相对基准',
    baselineTag: '基准',
    btnOpenChart: '打开完整图表',
    btnChallenge: '质疑 / 提出修正建议',
    challengeTitle: (id) => `针对参数提出建议：${id}`,
    phSuggested: (val) => `建议值或合理区间（当前默认：${val}）`,
    phNote: '请填写实证文献、广州一线经验或调整理由……',
    btnCopyNote: '复制结构化反馈给作者',
    noteCopied: '已复制结构化反馈到剪贴板。',
    permalink: '固定链接',
    srcTitle: '文献锚点、引用格式与数据溯源',
    srcLead: '主升学模型涵盖 1,024 组参数设定（每组 40,000 名合成学生）；修订后的补习选择模型涵盖 40 组设定与 2 个旧版基准，共 8 组配对样本（种子 2201–2208）。两套实验均采用合成队列，旨在明确假设前提下剥离制度与行为机制。',
    citeHeading: '引用本工作论文与数据集',
    citeDoiLabel: '数据集 DOI：',
    btnCopyApa: '复制 APA 引文',
    btnCopyBib: '复制 BibTeX',
    apaCopied: 'APA 引文已复制。',
    bibCopied: 'BibTeX 已复制。',
    dlHeading: '下载已校验的数据快照',
    dlData: '全部 14 个主题与已保存情境数据',
    dlAssump: '完整 134 项假设与参数清单',
    dlProv: '实验范围与 SHA-256 校验值',
    dlGithub: 'GitHub 工作论文归档（早期版本）',
    dlZenodo: 'Zenodo 教育图谱总合集',
    anchorsHeading: '核心实证与制度参考文献',
    provHeading: '密码学溯源校验（SHA-256）',
    provLead: '实时读取自 provenance.json，确保页面中展示的每一张图表都可一一对应到原始保存输出文件。',
    provColLayer: '层级',
    provColFile: '文件名',
    provColHash: 'SHA-256 哈希值',
    layerServed: '前端服务快照',
    layerSource: '模型原始汇总输出',
    footerLeft: '广州教育机会交互浏览器 · 修订版 1.4 · Dr. Trey Menefee',
    footerRepo: 'Atlas 开源仓库',
    loadError: '无法加载已保存的数据文件，请刷新页面重试。',
    storyCards: [
      {
        metric: '65.8% 对比 81.8%',
        title: '公办向上通道畅通，但财富差距显著',
        summary: '初始能力前10%的本地学生中，收入后40%群体约有三分之二进入重点大学通道，收入前40%群体约为五分之四。',
        topic: 'access', caseIdx: 2
      },
      {
        metric: '0.91 → 1.17 → 1.37',
        title: '为何不同口径下的公平比率截然相反',
        summary: '按中考分数比较时接近均等（0.91），因为家庭与初中优势早已内化于分数；改按初始能力比较，富裕优势升至1.37倍。',
        topic: 'fairness', caseIdx: 0
      },
      {
        metric: '58.2% → 70.4%',
        title: '早期优势的消退速度是最大杠杆',
        summary: '早期优势消退比例从 ≤15% 提高到 75–90%，贫困高能力学生的机会提升 12.2 个百分点——远超任何单一补习政策。',
        topic: 'fade', caseIdx: 5
      },
      {
        metric: '学期 0.08% → 24.7%',
        title: '高中住校将学期补习挤压至寒暑假',
        summary: '每周仅1小时可用空余时，高二住校生学期补习近乎为零，但寒暑假参与率仍达27.8%；若放宽至3小时，学期需求立即反弹。',
        topic: 'calendar', caseId: 'board_longer_term'
      },
      {
        metric: '29.5% → 35.0%',
        title: '家长预期本身就能推高补习需求',
        summary: '仅提高高二家庭对补习收益的预期，年参与率即上升5.5个百分点；仅提高真实提分效果而不改预期，购买行为毫无变化。',
        topic: 'grade', caseId: 'g11_belief_only_039'
      },
      {
        metric: '3.0%–9.8% 被挤落 · 高端1:1为零',
        title: '排位挤出随补习效力放大',
        summary: '统一限制补习在基准下仅增 +0.25 百分点，但富裕家庭补习仍将 3.0%–9.8% 贫困优生挤落排位档；年费120万一对一无买家。',
        topic: 'ranks', caseIdx: 3
      }
    ],
    topicGroups: {
      all: '全部研究问题 (14)',
      core: '升学机会与公平性',
      mech: '作用机制与补习限制',
      choice: '补习选择与时间景观',
      sens: '制度与能力敏感性'
    },
    models: {
      'Original Guangzhou model': '主升学模拟模型（原始设计）',
      'Revised tutoring choice': '家庭补习选择扩展模型'
    },
    groups: {
      'Simulation design and sensitivity': '模拟设计与敏感性',
      'Population and household resources': '人口结构与家庭资源',
      'School access and hukou': '入学通道与户籍规则',
      'School learning': '校内教学与同伴投入',
      'Tutoring and household choices': '校外补习与家庭选择',
      'Alternative university routes': '多元升学通道（艺考/联考）',
      'Outcomes and comparisons': '结果指标与比较口径'
    },
    topics: {
      access: {
        label: '谁能进入重点大学通道？',
        description: '主模型显示，广州公办体系为贫困高能力本地生提供了可观的向上通道，但与富裕群体之间仍存在稳定的财富差距。',
        metric: '进入模拟重点大学通道的比例（%）',
        series: ['收入后40%本地家庭', '收入前40%本地家庭'],
        interval: '已保存参数设定下的中位数与第5–95百分位区间'
      },
      fairness: {
        label: '中考分数能反映全部公平性吗？',
        description: '当按学生已经考出的中考分数分组比较时，家庭优势显得很小；一旦前移至初始能力口径，差距立刻拉大。',
        metric: '富贫重点大学通道比率（1.0 为完全均等）',
        series: ['富贫比率'],
        interval: '已保存参数设定下的中位数与第5–95百分位区间'
      },
      fade: {
        label: '早期学习优势能持续多久？',
        description: '在早期优势消退更多的参数组中，贫困高能力学生的升学机会显著上升。',
        metric: '进入模拟重点大学通道的比例（%）',
        series: ['收入后40%本地家庭', '收入前40%本地家庭'],
        interval: '各消退区间内的中位数与第5–95百分位区间'
      },
      inputs: {
        label: '哪些投入对贫困学生影响最大？',
        description: '在150组配对反事实实验中，家庭资源与初中片区师资差异的解释力远高于基准设定下的中考前补习。',
        metric: '进入模拟重点大学通道的比例（%）',
        series: ['收入后40%本地家庭', '收入前40%本地家庭'],
        interval: '150组配对设定下的中位数与第5–95百分位区间'
      },
      restriction: {
        label: '如果限制校外补习会怎样？',
        description: '限制政策的效果高度取决于补习的真实提分幅度，以及富裕家庭是否能够通过其他渠道规避限制。',
        metric: '贫困高能力生重点大学通道率平均变化（百分点）',
        series: ['各群体均等削减', '富裕家庭基本规避'],
        interval: '已保存设定与队列下的均值'
      },
      ranks: {
        label: '谁会被挤落排位档次？（修订选择模型）',
        description: '在学校与班级分配固定的前提下，扣除富裕家庭的模拟补习加分，观察贫困高能力生排位下滑的比例。',
        metric: '至少下滑一个排位档次的贫困高能力生比例（%）',
        series: ['至少下滑一档的比例'],
        interval: '8组配对队列种子的均值与最小–最大范围'
      },
      grade: {
        label: '按年级划分的年度补习参与率',
        description: '对比年度补习选择模型下的各已保存设定。每个阶段使用各自的分母，年度参与率按去重学生计算。',
        metric: '年度补习参与率（%）',
        series: ['初三（全部学生）', '高二（普通高中学术轨）'],
        interval: '8组配对队列种子的均值与最小–最大范围'
      },
      calendar: {
        label: '住校制度与补习“时间景观”',
        description: '对比住校生与走读生在学期内及寒暑假的补习参与率，观察作息窗口如何重塑校外补习的时间分布。',
        metric: '分时段补习参与率（%）',
        series: ['高二住校生（学期内）', '高二走读生（学期内）', '高二住校生（寒暑假）'],
        interval: '8组配对队列种子的均值与最小–最大范围'
      },
      wealth: {
        label: '哪些家庭在购买校外补习？',
        description: '比较本地户籍收入后40%与前40%家庭的高二年度补习参与率。',
        metric: '高二年度补习参与率（%）',
        series: ['本地收入后40%高二学生', '本地收入前40%高二学生'],
        interval: '8组配对队列种子的均值与最小–最大范围'
      },
      fulltime: {
        label: '家庭会购买全日制替代补习吗？',
        description: '合成市场中存在少量全日制小班买家，但年费120万元的高端一对一买家为零（受合成收入尾部分布与无借贷假设制约）。',
        metric: '每40,000人队列中的平均人数',
        series: ['全日制小班买家', '高端一对一买家', '预算可负担的高端邀约数'],
        interval: '8组配对队列种子的均值与最小–最大范围'
      },
      schools: {
        label: '引入216所真实校区清单是否改变结论？',
        description: '对比简化学校设定与基于广州216所校区招生计划的稳健性设计，贫困高能力群体的中位数结果非常接近。',
        metric: '进入模拟重点大学通道的比例（%）',
        series: ['收入后40%本地家庭', '收入前40%本地家庭'],
        interval: '已保存参数设定下的中位数与第5–95百分位区间'
      },
      skills: {
        label: '如果纳入第二项非认知能力权重会怎样？',
        description: '主模型对额外非认知能力赋予零权重；此处展示逐步提高其权重后的敏感性变化。',
        metric: '贫困本地生进入重点大学通道的比例（%）',
        series: ['认知能力前10%', '双项能力均在前10%'],
        interval: '已保存参数设定下的中位数与第5–95百分位区间'
      },
      hukou: {
        label: '非本地户籍学生的升学分流去向',
        description: '户籍名额限制影响公办普高录取，此处展示模型中非本地户籍学生在四类路径间的分布。',
        metric: '占非本地户籍学生的比例（%）',
        series: ['非本地户籍学生'],
        interval: '已保存参数设定下的中位数与第5–95百分位区间'
      },
      'ranks-legacy': {
        label: '旧版排位挤出压力测试（基准对比）',
        description: '此前常被引用的“六分之一”来自旧版强效假设；新旧两套补习菜单与效力设计产出不同量级。',
        metric: '至少下滑一个排位档次的贫困高能力生比例（%）',
        series: ['至少下滑一档的比例'],
        interval: '旧版参数设定下的均值与第5–95百分位区间'
      }
    }
  }
};
