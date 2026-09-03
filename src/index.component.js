<script type="text/x-dc" data-dc-script="" data-props="{&quot;$preview&quot;:{&quot;width&quot;:1440,&quot;height&quot;:1000},&quot;whatsappNumber&quot;:{&quot;editor&quot;:&quot;text&quot;,&quot;default&quot;:&quot;5561982777896&quot;,&quot;tsType&quot;:&quot;string&quot;,&quot;section&quot;:&quot;Contato&quot;},&quot;calendlyUrl&quot;:{&quot;editor&quot;:&quot;text&quot;,&quot;default&quot;:&quot;https://calendly.com/asfadvogados&quot;,&quot;tsType&quot;:&quot;string&quot;,&quot;section&quot;:&quot;Contato&quot;},&quot;defaultAreaTab&quot;:{&quot;editor&quot;:&quot;enum&quot;,&quot;default&quot;:&quot;concursos&quot;,&quot;tsType&quot;:&quot;string&quot;,&quot;options&quot;:[&quot;concursos&quot;,&quot;empresarial&quot;],&quot;section&quot;:&quot;Áreas de atuação&quot;}}">
class Component extends DCLogic {
  state = {
    mobileOpen: false,
    activeTab: 'concursos',
    openValor: 0,
    reviewIndex: 0,
    teamIndex: 0,
    windowWidth: typeof window !== 'undefined' ? window.innerWidth : 1280,
  };

  componentDidMount() {
    this._onResize = () => this.setState({ windowWidth: window.innerWidth });
    window.addEventListener('resize', this._onResize);
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this._onResize);
  }

  scrollToArea(tab) {
    this.setState({ activeTab: tab }, () => {
      const el = document.getElementById('areas');
      if (el) {
        const y = el.getBoundingClientRect().top + window.scrollY - 80;
        window.scrollTo({ top: y, behavior: 'smooth' });
      }
    });
  }

  renderVals() {
    const props = this.props || {};
    const whatsappNumber = props.whatsappNumber || '5561982777896';
    const calendlyUrl = props.calendlyUrl || 'https://calendly.com/asfadvogados';
    const defaultTab = props.defaultAreaTab || 'concursos';
    const activeTab = this.state.activeTab || defaultTab;
    const isMobile = this.state.windowWidth < 900;

    const concursosItemsRaw = [
      ['Recurso administrativo', 'Preparação técnica do recurso para reverter ilegalidades já na via administrativa.'],
      ['Processos judiciais', 'Atuação em todas as instâncias quando a via administrativa se esgota.'],
      ['Prova objetiva', 'Revisão de gabaritos com erros, divergências de edital ou questões ilegais.'],
      ['Prova discursiva', 'Contestação de correções subjetivas feitas em desacordo com o edital.'],
      ['Teste de aptidão física (TAF)', 'Reversão de reprovações por cronômetro fantasma, marcação incorreta e abusos na aplicação.'],
      ['Avaliação psicológica', 'Questionamento de laudos genéricos ou aplicados fora da técnica correta.'],
      ['Avaliação médica', 'Reversão judicial de laudos sem fundamentação ou com erros grosseiros.'],
      ['Investigação social', 'Suporte no preenchimento da FIC e defesa em caso de eliminação.'],
      ['Heteroidentificação', 'Análise de viabilidade para candidatos pardos ou negros eliminados na fase de cotas.'],
      ['Candidato PCD e autista', 'Defesa do acesso às vagas de cotas e reversão de eliminações injustas.'],
      ['Preterição arbitrária', 'Atuação contra a preterição de aprovados em favor de terceirizados.'],
      ['Vagas e nomeação', 'Proteção de vagas e nomeações ameaçadas por prazo, lista ou convocação.'],
    ];
    const servidoresItemsRaw = [
      ['Processo Administrativo Disciplinar (PAD)', 'Defesa técnica em todas as fases do PAD, revertendo ilegalidades praticadas por órgãos e comissões.'],
      ['Perseguição funcional', 'Atuação em casos de perseguição rotineira contra servidores, com argumentos sólidos para reverter o cenário.'],
      ['Cargos de direção e chefia', 'Experiência na defesa de gestores, diretores e servidores em cargos de confiança.'],
      ['Análise de viabilidade', 'Avaliação transparente da viabilidade administrativa ou judicial antes de qualquer ação — sem vender ilusão.'],
      ['Recurso administrativo e judicial', 'Atuação técnica para resguardar o cargo e reverter decisões ilegais em qualquer instância.'],
      ['Atendimento nacional', 'Processos 100% online: atendemos servidores públicos de todos os estados do Brasil.'],
    ];
    const empresarialItemsRaw = [
      ['Dívidas bancárias e empréstimos', 'Renegociação técnica para reduzir o peso das dívidas no caixa da empresa.'],
      ['Contratos bancários', 'Revisão de cláusulas abusivas em operações de crédito e financiamento.'],
      ['Capital de giro', 'Estratégias jurídicas para preservar o fluxo de caixa em momentos de aperto.'],
      ['Passivo tributário', 'Planejamento e defesa em autuações e cobranças de impostos.'],
      ['Reestruturação de passivos', 'Reorganização das dívidas da empresa para viabilizar a continuidade do negócio.'],
      ['Proteção jurídica empresarial', 'Blindagem preventiva do patrimônio e das operações da empresa.'],
      ['Empresário endividado', 'Suporte jurídico para quem responde pessoalmente por dívidas do negócio.'],
      ['Perdas nos negócios', 'Reestruturação e defesa em cenários de queda de faturamento e crise.'],
    ];
    const toItems = (raw) => raw.map((r, i) => ({ num: String(i + 1).padStart(2, '0'), title: r[0], desc: r[1] }));

    const valoresRaw = [
      ['01', 'Transparência', 'Direcionamos cada caso conforme a verdade do que acreditamos — mesmo quando a melhor orientação é aguardar ou não entrar com a ação. Somos responsáveis com o seu tempo e o seu dinheiro.'],
      ['02', 'Acolhimento', 'Entrar com uma ação é um momento delicado. Por isso, atendemos com empatia e humanidade, para que a sua luta nunca seja solitária.'],
      ['03', 'Atendimento', 'Mais de 44% dos clientes já tiveram experiências negativas com escritórios de advocacia. Nosso compromisso é ressignificar essa experiência desde o primeiro contato.'],
      ['04', 'Comprometimento e perseverança', 'Buscamos constante atualização técnica e as melhores jurisprudências para defender nossos clientes — e lutamos em todas as instâncias necessárias.'],
      ['05', 'Comunicação clara e ética', 'Você deve entender cada etapa do seu processo. A ética é a bússola que guia tudo o que fazemos.'],
    ];
    const openValor = this.state.openValor;
    const valores = valoresRaw.map((v, i) => ({
      num: v[0], title: v[1], text: v[2],
      open: openValor === i,
      indicator: openValor === i ? '\u2212' : '+',
      toggle: () => this.setState((s) => ({ openValor: s.openValor === i ? -1 : i })),
    }));

    const team = [
      { name: 'Dr. Silas Adauto', role: 'Especialista na proteção jurídica de empresas', oab: '', photo: 'uploads/silas.fw.png', initials: '' },
      { name: 'Dra Nayara França', role: 'Sócia fundadora', oab: '', photo: 'uploads/nayara.fw.png', initials: '' },
      { name: 'Dr. Bruno Gabriel', role: 'Advogado Especialista em Direito Público e Estratégia Empresarial', oab: '', photo: 'uploads/gabriel.jpeg', initials: '' },
      { name: 'Dr. Flávio Augusto', role: 'Especialista em Instituições Bancárias | Ex-Gerente de Alta Renda', oab: '', photo: 'uploads/FlavioAugusto.jpeg', initials: '' },
      { name: 'Dra. Danielle Batista', role: 'Advogada e Controller Estratégica', oab: '', photo: 'uploads/DanielleBatista.jpeg', initials: '' },
      { name: 'Thaís Santos', role: 'Marketing', oab: '', photo: 'uploads/opt/IMG_4884.jpg', initials: '' },
      { name: 'Vitória', role: 'Controladoria Jurídica', oab: '', photo: 'uploads/opt/IMG_4973_1-82c496cf.jpg', initials: '' },
      { name: 'Rebeca', role: 'Marketing', oab: '', photo: 'uploads/opt/IMG_5119_1.jpg', initials: '' },
    ];

    const reviews = [
      { name: 'João Vitor', text: 'Não há adjetivos que possam descrever a gratidão que tenho ao escritório ASF Advogados. Desde o início, o Dr. Bruno teve total empatia e paciência em me explicar cada parte do processo.' },
      { name: 'Juciara Mota', text: 'Fui atendida com prontidão, cortesia e rapidez. Silas demonstrou amplo conhecimento técnico e segurança na condução do caso — a liminar foi concedida em cerca de três horas.' },
      { name: 'Luí Campos', text: 'O trabalho de vocês foi simplesmente excepcional. Demonstraram um preparo técnico gigante, rebatendo ponto a ponto a injustiça da minha eliminação.' },
      { name: 'Giovanna Santos', text: 'Elogio ao Dr. Silas, muito atencioso no meu caso e que não mediu esforços para ganhar a causa. Graças ao trabalho desses profissionais, fui reintegrada no meu concurso.' },
      { name: 'Raylane Martins', text: 'Trabalho impecável do Bruno e do Silas. Em um momento de muita ansiedade, me acolheram, ouviram e me passaram toda a segurança que eu precisava.' },
    ];
    const articles = [
      { tag: 'Concursos', title: 'Reprovei no TAF. Dá para reverter?', excerpt: 'Cronômetro fantasma, marcação incorreta e regras alteradas no meio do certame. Veja o que fazer antes de judicializar.', href: 'artigos.html#taf' },
      { tag: 'Concursos', title: 'Recurso administrativo: a primeira linha de defesa', excerpt: 'Por que preparar um recurso técnico logo no início do certame pode mudar todo o resultado.', href: 'artigos.html#recurso' },
      { tag: 'Empresarial', title: 'Dívidas bancárias e capital de giro na crise', excerpt: 'Como reestruturar passivos sem comprometer a operação e o crescimento da empresa.', href: 'artigos.html#dividas' },
    ];

    const tabBtnBase = 'padding:13px 26px;border-radius:999px;font-family:Manrope,sans-serif;font-weight:700;font-size:13px;letter-spacing:.03em;cursor:pointer;border:1px solid rgba(22,20,15,0.18);transition:all .25s ease;';
    const concursosTabStyle = tabBtnBase + (activeTab === 'concursos' ? 'background:#16140F;color:#F5EFE3;border-color:#16140F;' : 'background:transparent;color:#16140F;');
    const servidoresTabStyle = tabBtnBase + (activeTab === 'servidores' ? 'background:#16140F;color:#F5EFE3;border-color:#16140F;' : 'background:transparent;color:#16140F;');
    const empresarialTabStyle = tabBtnBase + (activeTab === 'empresarial' ? 'background:#16140F;color:#F5EFE3;border-color:#16140F;' : 'background:transparent;color:#16140F;');

    const desktopNavStyle = 'display:' + (isMobile ? 'none' : 'flex') + ';align-items:center;gap:30px;';
    const hamburgerStyle = 'display:' + (isMobile ? 'flex' : 'none') + ';flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:8px;';
    const mobilePanelStyle = 'display:' + (isMobile && this.state.mobileOpen ? 'flex' : 'none') + ';position:fixed;inset:0;z-index:100;background:#16140F;flex-direction:column;padding:28px 32px;gap:8px;overflow-y:auto;';
    const headerCtaStyle = 'display:' + (isMobile ? 'none' : 'inline-flex') + ';align-items:center;gap:10px;padding:12px 22px;border-radius:999px;background:#16140F;color:#F5EFE3;text-decoration:none;font-family:Manrope,sans-serif;font-weight:700;font-size:13px;white-space:nowrap;';

    const cardW = 320;
    const gapW = 20;
    const viewportW = Math.max(280, Math.min(this.state.windowWidth, 1280) - 64);
    const visibleCount = Math.max(1, Math.floor((viewportW + gapW) / (cardW + gapW)));
    const maxReviewIndex = Math.max(0, reviews.length - visibleCount);
    const reviewIndex = Math.min(this.state.reviewIndex || 0, maxReviewIndex);
    const reviewTrackStyle = 'display:flex;gap:' + gapW + 'px;transition:transform .45s ease;transform:translateX(-' + (reviewIndex * (cardW + gapW)) + 'px);';
    const canPrevReview = reviewIndex > 0;
    const canNextReview = reviewIndex < maxReviewIndex;
    const arrowBase = 'width:44px;height:44px;border-radius:50%;border:1px solid rgba(22,20,15,0.18);background:#F5EFE3;font-size:16px;';
    const prevReview = () => this.setState((s) => ({ reviewIndex: Math.max(0, (s.reviewIndex || 0) - 1) }));
    const nextReview = () => this.setState((s) => ({ reviewIndex: Math.min(maxReviewIndex, (s.reviewIndex || 0) + 1) }));
    const prevReviewStyle = arrowBase + (canPrevReview ? 'cursor:pointer;color:#16140F;' : 'cursor:default;color:#C9C2B3;');
    const nextReviewStyle = arrowBase + (canNextReview ? 'cursor:pointer;color:#16140F;' : 'cursor:default;color:#C9C2B3;');

    const teamCardW = 240;
    const teamGapW = 24;
    const teamViewportW = Math.max(240, Math.min(this.state.windowWidth, 1280) - 64);
    const teamVisibleCount = Math.max(1, Math.floor((teamViewportW + teamGapW) / (teamCardW + teamGapW)));
    const maxTeamIndex = Math.max(0, team.length - teamVisibleCount);
    const teamIndex = Math.min(this.state.teamIndex || 0, maxTeamIndex);
    const teamTrackStyle = 'display:flex;gap:' + teamGapW + 'px;transition:transform .45s ease;transform:translateX(-' + (teamIndex * (teamCardW + teamGapW)) + 'px);';
    const canPrevTeam = teamIndex > 0;
    const canNextTeam = teamIndex < maxTeamIndex;
    const teamArrowBase = 'width:44px;height:44px;border-radius:50%;border:1px solid rgba(245,239,227,0.3);background:transparent;font-size:16px;';
    const prevTeam = () => this.setState((s) => ({ teamIndex: Math.max(0, (s.teamIndex || 0) - 1) }));
    const nextTeam = () => this.setState((s) => ({ teamIndex: Math.min(maxTeamIndex, (s.teamIndex || 0) + 1) }));
    const prevTeamStyle = teamArrowBase + (canPrevTeam ? 'cursor:pointer;color:#F5EFE3;' : 'cursor:default;color:#5A5648;');
    const nextTeamStyle = teamArrowBase + (canNextTeam ? 'cursor:pointer;color:#F5EFE3;' : 'cursor:default;color:#5A5648;');

    const whatsappMsg = encodeURIComponent('Olá! Vim pelo site e gostaria de falar com a ASF Advogados.');
    const whatsappLink = 'https://wa.me/' + whatsappNumber + '?text=' + whatsappMsg;
    const areaWhatsapp = (area) => 'https://wa.me/' + whatsappNumber + '?text=' + encodeURIComponent('Olá! Vim pelo site e gostaria de saber mais sobre a área de ' + area + '.');
    const concursosWhatsapp = areaWhatsapp('Concursos');
    const servidoresWhatsapp = areaWhatsapp('Servidores Públicos');
    const empresarialWhatsapp = areaWhatsapp('Direito Empresarial');

    return {
      mobileOpen: this.state.mobileOpen,
      toggleMobile: () => this.setState((s) => ({ mobileOpen: !s.mobileOpen })),
      closeMobile: () => this.setState({ mobileOpen: false }),
      desktopNavStyle, hamburgerStyle, mobilePanelStyle, headerCtaStyle,
      isConcursos: activeTab === 'concursos',
      isServidores: activeTab === 'servidores',
      isEmpresarial: activeTab === 'empresarial',
      setConcursos: () => this.setState({ activeTab: 'concursos' }),
      setServidores: () => this.setState({ activeTab: 'servidores' }),
      setEmpresarial: () => this.setState({ activeTab: 'empresarial' }),
      goToConcursos: () => this.scrollToArea('concursos'),
      goToServidores: () => this.scrollToArea('servidores'),
      goToEmpresarial: () => this.scrollToArea('empresarial'),
      concursosTabStyle, servidoresTabStyle, empresarialTabStyle,
      concursosItems: toItems(concursosItemsRaw),
      servidoresItems: toItems(servidoresItemsRaw),
      empresarialItems: toItems(empresarialItemsRaw),
      valores, team, articles, reviews,
      reviewTrackStyle, prevReview, nextReview, prevReviewStyle, nextReviewStyle,
      teamTrackStyle, prevTeam, nextTeam, prevTeamStyle, nextTeamStyle,
      whatsappLink,
      concursosWhatsapp, servidoresWhatsapp, empresarialWhatsapp,
      whatsappDisplay: '(61) 98277-7896',
      calendlyLink: calendlyUrl,
      year: new Date().getFullYear(),
    };
  }
}
</script>
