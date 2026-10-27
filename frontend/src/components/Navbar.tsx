import React, { useState, useEffect } from 'react';
import { Leaf, Menu, X, ChevronRight, Activity } from 'lucide-react';
import { checkHealth, type HealthResponse } from '../lib/api';

interface NavbarProps {
  activeSection: string;
  onNavigate: (sectionId: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeSection, onNavigate }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    checkHealth()
      .then(setHealth)
      .catch(() => setHealth(null));

    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { id: 'identify', label: 'Identify' },
    { id: 'performance', label: 'Performance' },
    { id: 'species', label: 'Species' },
    { id: 'about', label: 'About' },
  ];

  const handleNavClick = (id: string) => {
    setMobileMenuOpen(false);
    onNavigate(id);
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-[#06140E]/85 backdrop-blur-xl border-b border-white/[0.08] shadow-2xl py-3.5'
          : 'bg-transparent py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          {/* Brand Logo */}
          <button
            onClick={() => handleNavClick('hero')}
            className="flex items-center gap-3 text-left focus:outline-none group cursor-pointer"
            aria-label="Van Udyan Plant AI Home"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#2D6A4F] to-[#0F2A1E] border border-[#52B788]/30 flex items-center justify-center shadow-lg group-hover:border-[#52B788]/60 transition-colors">
              <Leaf className="w-5 h-5 text-[#52B788] group-hover:rotate-12 transition-transform duration-300" />
            </div>
            <div>
              <div className="font-heading font-extrabold text-sm tracking-widest uppercase text-white flex items-center gap-1.5">
                Van Udyan <span className="text-[#C9A227] font-semibold text-xs tracking-normal">AI</span>
              </div>
              <div className="text-[10px] tracking-wider uppercase text-emerald-400/80 font-medium">
                Urban Plant Vision
              </div>
            </div>
          </button>

          {/* Desktop Nav Links */}
          <nav className="hidden md:flex items-center gap-1 bg-[#102a1e]/60 p-1.5 rounded-full border border-white/[0.08] backdrop-blur-md">
            {navLinks.map((link) => {
              const isActive = activeSection === link.id;
              return (
                <button
                  key={link.id}
                  onClick={() => handleNavClick(link.id)}
                  className={`px-4 py-1.5 rounded-full text-xs font-semibold tracking-wide transition-all duration-200 cursor-pointer ${
                    isActive
                      ? 'bg-[#52B788] text-[#06140E] shadow-md shadow-[#52B788]/20'
                      : 'text-slate-300 hover:text-white hover:bg-white/[0.05]'
                  }`}
                >
                  {link.label}
                </button>
              );
            })}
          </nav>

          {/* Diagnostics Status Pill */}
          <div className="hidden lg:flex items-center gap-2">
            <div className="flex items-center gap-2 bg-[#143D2A]/50 border border-emerald-500/20 px-3 py-1.5 rounded-full text-xs">
              <span className="relative flex h-2 w-2">
                <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${health?.model_loaded ? 'bg-emerald-400' : 'bg-amber-400'}`}></span>
                <span className={`relative inline-flex rounded-full h-2 w-2 ${health?.model_loaded ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
              </span>
              <span className="text-slate-300 font-medium text-[11px]">
                {health?.model_loaded ? 'EfficientNetB0 Active' : 'Connecting to Core...'}
              </span>
            </div>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-xl bg-white/[0.05] border border-white/[0.08] text-slate-300 hover:text-white focus:outline-none cursor-pointer"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden mt-3 px-4 pt-2 pb-4 bg-[#0A1E15]/95 backdrop-blur-2xl border-b border-white/[0.08] shadow-2xl">
          <div className="flex flex-col gap-2">
            {navLinks.map((link) => (
              <button
                key={link.id}
                onClick={() => handleNavClick(link.id)}
                className={`flex items-center justify-between px-4 py-3 rounded-xl text-sm font-semibold tracking-wide text-left cursor-pointer ${
                  activeSection === link.id
                    ? 'bg-[#52B788] text-[#06140E]'
                    : 'text-slate-300 hover:bg-white/[0.05]'
                }`}
              >
                <span>{link.label}</span>
                <ChevronRight className="w-4 h-4 opacity-60" />
              </button>
            ))}
            <div className="mt-3 pt-3 border-t border-white/[0.08] flex items-center justify-between px-2">
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <Activity className="w-3.5 h-3.5 text-emerald-400" />
                <span>{health?.model_loaded ? 'Neural Engine Online' : 'Connecting...'}</span>
              </div>
              <span className="text-[10px] text-emerald-400 font-mono">Top-15 EfficientNet</span>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};
