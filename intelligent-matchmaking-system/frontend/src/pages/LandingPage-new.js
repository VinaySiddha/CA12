import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <>
      <div className="px-4 py-16">
        <div className="@container">
          <div className="p-4">
            <div className="flex min-h-[480px] flex-col gap-8 rounded-xl items-center justify-center p-4 relative overflow-hidden" data-alt="Abstract gradient background with soft hues of purple and blue">
              <div className="absolute inset-0 bg-gradient-to-br from-[#8A2BE2]/20 to-[#4B0082]/20 dark:from-[#8A2BE2]/30 dark:to-[#4B0082]/30 animate-pulse"></div>
              <div className="absolute inset-0" style={{backgroundImage: 'radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px)', backgroundSize: '20px 20px'}}></div>
              <div className="flex flex-col gap-4 text-center z-10">
                <h1 className="text-[#111318] dark:text-white text-5xl font-black leading-tight tracking-[-0.033em]">
                  Intelligent Matchmaking for Professionals
                </h1>
                <h2 className="text-[#111318] dark:text-white/80 text-base font-normal leading-normal max-w-2xl mx-auto">
                  Harnessing AI to connect you with your ideal peer for collaboration, mentorship, and growth.
                </h2>
              </div>
              <Link to="/register" className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-5 bg-gradient-to-r from-[#8A2BE2] to-[#4B0082] text-white text-base font-bold leading-normal tracking-[0.015em] hover:opacity-90 transition-opacity z-10 shadow-lg shadow-[#8A2BE2]/20">
                <span className="truncate">Find Your Ideal Peer</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
      
      <section className="px-4 py-16">
        <h2 className="text-[#111318] dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5 text-center">Our Mission</h2>
        <p className="text-[#111318] dark:text-white/80 text-base font-normal leading-normal pb-3 pt-1 px-4 text-center max-w-3xl mx-auto">
          We are dedicated to fostering meaningful professional connections through our intelligent, data-driven matchmaking platform. Our mission is to empower individuals to achieve their career goals by connecting them with the right peers for collaboration, mentorship, and mutual growth.
        </p>
        <div className="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-6 p-4 mt-8">
          <div className="flex flex-1 gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 flex-col items-center text-center backdrop-blur-md hover:border-primary/50 dark:hover:border-primary/50 transition-all duration-300 transform hover:-translate-y-1">
            <div className="text-primary">
              <span className="material-symbols-outlined" style={{fontSize: '36px'}}>lightbulb</span>
            </div>
            <div className="flex flex-col gap-1">
              <h3 className="text-[#111318] dark:text-white text-lg font-bold leading-tight">Intelligence</h3>
              <p className="text-[#616b89] dark:text-white/70 text-sm font-normal leading-normal">
                Our AI-powered algorithm ensures precise and relevant matches based on skills, experience, and professional goals.
              </p>
            </div>
          </div>
          <div className="flex flex-1 gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 flex-col items-center text-center backdrop-blur-md hover:border-primary/50 dark:hover:border-primary/50 transition-all duration-300 transform hover:-translate-y-1">
            <div className="text-primary">
              <span className="material-symbols-outlined" style={{fontSize: '36px'}}>shield</span>
            </div>
            <div className="flex flex-col gap-1">
              <h3 className="text-[#111318] dark:text-white text-lg font-bold leading-tight">Trust</h3>
              <p className="text-[#616b89] dark:text-white/70 text-sm font-normal leading-normal">
                We prioritize the security and privacy of our users, creating a safe and trustworthy environment for networking.
              </p>
            </div>
          </div>
          <div className="flex flex-1 gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 flex-col items-center text-center backdrop-blur-md hover:border-primary/50 dark:hover:border-primary/50 transition-all duration-300 transform hover:-translate-y-1">
            <div className="text-primary">
              <span className="material-symbols-outlined" style={{fontSize: '36px'}}>groups</span>
            </div>
            <div className="flex flex-col gap-1">
              <h3 className="text-[#111318] dark:text-white text-lg font-bold leading-tight">Collaboration</h3>
              <p className="text-[#616b89] dark:text-white/70 text-sm font-normal leading-normal">
                We believe in the power of collaboration to drive innovation and success, connecting professionals who can achieve more together.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      <section className="px-4 py-16">
        <h2 className="text-[#111318] dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-8 pt-5 text-center">Testimonials</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-gray-300 flex items-center justify-center">
                <span className="material-symbols-outlined">person</span>
              </div>
              <div>
                <p className="font-bold text-[#111318] dark:text-white">Sarah Johnson</p>
                <p className="text-sm text-[#616b89] dark:text-white/70">Project Manager</p>
              </div>
            </div>
            <p className="text-[#111318] dark:text-white/80 text-base font-normal leading-normal italic">"This platform connected me with a mentor who completely changed my career trajectory. The matching was incredibly accurate!"</p>
          </div>
          <div className="flex flex-col gap-4 rounded-xl border border-[#dbdee6]/20 dark:border-[#dbdee6]/10 bg-white/50 dark:bg-black/20 p-6 backdrop-blur-md">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-gray-300 flex items-center justify-center">
                <span className="material-symbols-outlined">person</span>
              </div>
              <div>
                <p className="font-bold text-[#111318] dark:text-white">Michael Chen</p>
                <p className="text-sm text-[#616b89] dark:text-white/70">Software Engineer</p>
              </div>
            </div>
            <p className="text-[#111318] dark:text-white/80 text-base font-normal leading-normal italic">"Finding a co-founder with a complementary skillset was seamless. We launched our startup within six months of meeting here."</p>
          </div>
        </div>
      </section>
      
      <section className="px-4 py-16">
        <div className="rounded-xl p-8 bg-gradient-to-r from-primary to-[#8A2BE2] text-center flex flex-col items-center gap-6">
          <h2 className="text-white text-3xl font-bold leading-tight tracking-[-0.015em]">Ready to find your perfect match?</h2>
          <p className="text-white/80 text-base font-normal leading-normal max-w-xl">Join our network of professionals and start building meaningful connections today. Your next big opportunity is just a click away.</p>
          <Link to="/register" className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-5 bg-white text-primary text-base font-bold leading-normal tracking-[0.015em] hover:bg-white/90 transition-colors shadow-lg">
            <span className="truncate">Join Our Network</span>
          </Link>
        </div>
      </section>
    </>
  );
};

export default LandingPage;