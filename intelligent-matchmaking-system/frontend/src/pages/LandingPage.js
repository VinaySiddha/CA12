import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  AcademicCapIcon, 
  UsersIcon, 
  LightBulbIcon, 
  ChartBarIcon,
  StarIcon,
  ArrowRightIcon,
  SparklesIcon,
  BookOpenIcon,
  UserGroupIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline';
import GlassCard from '../components/ui/GlassCard';
import GlassButton from '../components/ui/GlassButton';

const LandingPage = () => {
  const features = [
    {
      icon: UsersIcon,
      title: 'Smart Peer Matching',
      description: 'AI-powered algorithms connect you with ideal study partners based on your learning style, interests, and goals.',
      color: 'text-primary-400',
    },
    {
      icon: AcademicCapIcon,
      title: 'Dynamic Study Groups',
      description: 'Join or create study groups that adapt to your schedule and learning objectives automatically.',
      color: 'text-secondary-400',
    },
    {
      icon: LightBulbIcon,
      title: 'Personalized Resources',
      description: 'Get curated learning materials and resources tailored to your academic needs and progress.',
      color: 'text-accent-400',
    },
    {
      icon: ChartBarIcon,
      title: 'Progress Tracking',
      description: 'Monitor your learning journey with detailed analytics and feedback from your study sessions.',
      color: 'text-green-400',
    },
    {
      icon: SparklesIcon,
      title: 'Gamified Learning',
      description: 'Earn points, badges, and achievements as you participate in collaborative learning experiences.',
      color: 'text-yellow-400',
    },
    {
      icon: GlobeAltIcon,
      title: 'Global Community',
      description: 'Connect with learners worldwide and expand your knowledge through diverse perspectives.',
      color: 'text-pink-400',
    },
  ];

  const stats = [
    { number: '10,000+', label: 'Active Learners', icon: UserGroupIcon },
    { number: '50,000+', label: 'Study Sessions', icon: BookOpenIcon },
    { number: '95%', label: 'Success Rate', icon: StarIcon },
    { number: '24/7', label: 'Learning Support', icon: LightBulbIcon },
  ];

  const testimonials = [
    {
      name: 'Sarah Chen',
      role: 'Computer Science Student',
      avatar: '👩‍💻',
      content: 'This platform transformed my learning experience. I found amazing study partners who helped me excel in machine learning!',
      rating: 5,
    },
    {
      name: 'Alex Rodriguez',
      role: 'Physics Graduate',
      avatar: '👨‍🔬',
      content: 'The AI matching is incredible. I connected with peers who perfectly complemented my strengths and weaknesses.',
      rating: 5,
    },
    {
      name: 'Emily Johnson',
      role: 'Psychology Major',
      avatar: '👩‍🎓',
      content: 'Study groups here are so well-organized. The progress tracking keeps me motivated and on track with my goals.',
      rating: 5,
    },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
      },
    },
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative py-20">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center max-w-4xl mx-auto"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            <motion.h1
              className="text-5xl md:text-7xl font-bold text-black mb-6"
              variants={itemVariants}
            >
              Learn{' '}
              <span className="text-primary-500">
                Together
              </span>
              <br />
              Grow{' '}
              <span className="text-primary-600">
                Faster
              </span>
            </motion.h1>

            <motion.p
              className="text-xl md:text-2xl text-gray-700 mb-8 leading-relaxed"
              variants={itemVariants}
            >
              Join the next generation of collaborative learning. Connect with perfect study partners,
              form dynamic groups, and accelerate your academic journey with AI-powered matching.
            </motion.p>

            <motion.div
              className="flex flex-col sm:flex-row gap-4 justify-center"
              variants={itemVariants}
            >
              <Link to="/register">
                <GlassButton size="lg" variant="primary" className="group">
                  Get Started Free
                  <ArrowRightIcon className="w-5 h-5 ml-2 transition-transform group-hover:translate-x-1" />
                </GlassButton>
              </Link>
              <Link to="/login">
                <GlassButton size="lg" variant="ghost">
                  Sign In
                </GlassButton>
              </Link>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <motion.div
            className="grid grid-cols-2 md:grid-cols-4 gap-6"
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {stats.map((stat, index) => (
              <motion.div key={index} variants={itemVariants}>
                <GlassCard className="text-center">
                  <stat.icon className="w-8 h-8 mx-auto mb-3 text-primary-400" />
                  <div className="text-3xl font-bold text-black mb-2">{stat.number}</div>
                  <div className="text-gray-600">{stat.label}</div>
                </GlassCard>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Why Choose{' '}
              <span className="text-primary-500">
                LearnTogether
              </span>
            </h2>
            <p className="text-xl text-gray-700 max-w-2xl mx-auto">
              Experience the future of collaborative learning with cutting-edge AI technology
              and a vibrant community of passionate learners.
            </p>
          </motion.div>

          <motion.div
            className="grid md:grid-cols-2 lg:grid-cols-3 gap-8"
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {features.map((feature, index) => (
              <motion.div key={index} variants={itemVariants}>
                <GlassCard hover className="h-full">
                  <feature.icon className={`w-12 h-12 mb-4 ${feature.color}`} />
                  <h3 className="text-xl font-semibold text-black mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-700 leading-relaxed">
                    {feature.description}
                  </p>
                </GlassCard>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              What Our{' '}
              <span className="text-primary-500">
                Learners
              </span>{' '}
              Say
            </h2>
            <p className="text-xl text-gray-700 max-w-2xl mx-auto">
              Join thousands of students who have transformed their learning experience
              through collaborative partnerships.
            </p>
          </motion.div>

          <motion.div
            className="grid md:grid-cols-3 gap-8"
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {testimonials.map((testimonial, index) => (
              <motion.div key={index} variants={itemVariants}>
                <GlassCard hover>
                  <div className="flex items-center mb-4">
                    <span className="text-3xl mr-3">{testimonial.avatar}</span>
                    <div>
                      <h4 className="text-black font-semibold">{testimonial.name}</h4>
                      <p className="text-gray-600 text-sm">{testimonial.role}</p>
                    </div>
                  </div>
                  
                  <div className="flex mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <StarIcon key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  
                  <p className="text-gray-700 italic">"{testimonial.content}"</p>
                </GlassCard>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <GlassCard className="max-w-3xl mx-auto" glow>
              <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
                Ready to Start Your{' '}
                <span className="text-primary-500">
                  Learning Journey
                </span>
                ?
              </h2>
              
              <p className="text-xl text-gray-700 mb-8">
                Join thousands of students already using LearnTogether to achieve their academic goals.
                No credit card required.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/register">
                  <GlassButton size="lg" variant="primary" className="group">
                    Start Learning Today
                    <SparklesIcon className="w-5 h-5 ml-2 transition-transform group-hover:rotate-12" />
                  </GlassButton>
                </Link>
                <Link to="/login">
                  <GlassButton size="lg" variant="outline">
                    Explore Features
                  </GlassButton>
                </Link>
              </div>
            </GlassCard>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;