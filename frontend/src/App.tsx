import { useState, useEffect, lazy, Suspense } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { StatsStrip } from './components/StatsStrip';
import { BentoFeatures } from './components/BentoFeatures';
import { IdentifyPlant } from './components/IdentifyPlant';
import { Footer } from './components/Footer';

// Code-split sections
const PerformanceSection = lazy(() =>
  import('./components/PerformanceSection').then((m) => ({ default: m.PerformanceSection }))
);
const SpeciesGuide = lazy(() =>
  import('./components/SpeciesGuide').then((m) => ({ default: m.SpeciesGuide }))
);
const AboutSection = lazy(() =>
  import('./components/AboutSection').then((m) => ({ default: m.AboutSection }))
);

import { 
  fetchSpecies, 
  fetchMetrics, 
  type SpeciesResponse, 
  type MetricsResponse 
} from './lib/api';

export function App() {
  const [activeSection, setActiveSection] = useState('hero');
  const [speciesData, setSpeciesData] = useState<SpeciesResponse | null>(null);
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);

  useEffect(() => {
    Promise.allSettled([fetchSpecies(), fetchMetrics()]).then(([specRes, metRes]) => {
      if (specRes.status === 'fulfilled') {
        setSpeciesData(specRes.value);
      }
      if (metRes.status === 'fulfilled') {
        setMetrics(metRes.value);
      }
    });

    const sections = ['hero', 'identify', 'performance', 'species', 'about'];
    const handleScroll = () => {
      const scrollPos = window.scrollY + 200;
      for (const sectionId of sections) {
        const el = document.getElementById(sectionId);
        if (el) {
          const top = el.offsetTop;
          const height = el.offsetHeight;
          if (scrollPos >= top && scrollPos < top + height) {
            setActiveSection(sectionId);
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleNavigate = (sectionId: string) => {
    setActiveSection(sectionId);
    if (sectionId === 'hero') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }
    const element = document.getElementById(sectionId);
    if (element) {
      const offset = 80;
      const bodyRect = document.body.getBoundingClientRect().top;
      const elementRect = element.getBoundingClientRect().top;
      const elementPosition = elementRect - bodyRect;
      const offsetPosition = elementPosition - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  };

  return (
    <div className="min-h-screen bg-[#06140E] text-[#e2e8f0] relative selection:bg-[#52B788]/30 selection:text-[#B7C56A]">
      {/* Sticky Top Glass Navbar */}
      <Navbar
        activeSection={activeSection}
        onNavigate={handleNavigate}
      />

      <main>
        {/* Hero Section with Parallax Leaves */}
        <div id="hero">
          <Hero
            onIdentifyClick={() => handleNavigate('identify')}
            onPerformanceClick={() => handleNavigate('performance')}
          />
        </div>

        {/* Live Empirical Stats Strip */}
        <StatsStrip
          metrics={metrics}
          speciesData={speciesData}
        />

        {/* Bento Features Grid (2x3 dark-green, terracotta, sage) */}
        <BentoFeatures />

        {/* Interactive Neural Classifier Section */}
        <IdentifyPlant />

        {/* Lazy Loaded Code-Split Sections with Suspense */}
        <Suspense
          fallback={
            <div className="py-20 flex justify-center items-center">
              <div className="w-8 h-8 rounded-full border-2 border-[#52B788] border-t-transparent animate-spin" />
            </div>
          }
        >
          {/* Performance & Empirical Evaluation Section */}
          <PerformanceSection
            metrics={metrics}
          />

          {/* 15 Species Botanical Guide & Detail Modal */}
          <SpeciesGuide
            speciesList={speciesData?.species || []}
          />

          {/* About, RSWF Partnership & Data Provenance */}
          <AboutSection />
        </Suspense>
      </main>

      {/* Clean Dark Forest Footer */}
      <Footer
        onNavigate={handleNavigate}
      />
    </div>
  );
}

export default App;
