"""
Initialize database with AI/ML System Design Roadmap data
"""
from sqlalchemy.orm import Session
from backend.app.db import SessionLocal, init_db
from backend.app.models import Phase, Topic, Subtopic, MasteryComponent, Achievement, Stats


def seed_data():
    """Seed the database with initial AI/ML roadmap data"""
    init_db()
    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(Phase).count() > 0:
            print("Database already seeded. Skipping...")
            return

        # Create 10 Phases of AI/ML System Design Roadmap
        phases_data = [
            {
                "name": "Phase 1: Core CS Foundations",
                "description": "Master fundamental computer science concepts essential for AI/ML systems",
                "order": 1,
                "topics": [
                    {
                        "name": "Data Structures & Algorithms",
                        "description": "Arrays, LinkedLists, Trees, Graphs, Sorting, Searching",
                        "order": 1,
                        "subtopics": [
                            {"name": "Arrays and Strings", "order": 1},
                            {"name": "Linked Lists", "order": 2},
                            {"name": "Trees and Graphs", "order": 3},
                            {"name": "Sorting Algorithms", "order": 4},
                        ],
                    },
                    {
                        "name": "System Design Basics",
                        "description": "Scalability, Load Balancing, Caching, Database Design",
                        "order": 2,
                        "subtopics": [
                            {"name": "Horizontal vs Vertical Scaling", "order": 1},
                            {"name": "Load Balancers", "order": 2},
                            {"name": "Caching Strategies", "order": 3},
                        ],
                    },
                ],
            },
            {
                "name": "Phase 2: Mathematics for ML",
                "description": "Mathematical foundations for machine learning",
                "order": 2,
                "topics": [
                    {
                        "name": "Linear Algebra",
                        "description": "Vectors, Matrices, Eigenvalues, SVD",
                        "order": 1,
                        "subtopics": [
                            {"name": "Vectors and Vector Spaces", "order": 1},
                            {"name": "Matrix Operations", "order": 2},
                            {"name": "Eigenvalues and Eigenvectors", "order": 3},
                        ],
                    },
                    {
                        "name": "Probability & Statistics",
                        "description": "Distributions, Bayesian Inference, Hypothesis Testing",
                        "order": 2,
                        "subtopics": [
                            {"name": "Probability Distributions", "order": 1},
                            {"name": "Bayesian Statistics", "order": 2},
                            {"name": "Statistical Testing", "order": 3},
                        ],
                    },
                    {
                        "name": "Calculus & Optimization",
                        "description": "Derivatives, Gradients, Optimization Algorithms",
                        "order": 3,
                        "subtopics": [
                            {"name": "Derivatives and Gradients", "order": 1},
                            {"name": "Gradient Descent", "order": 2},
                            {"name": "Advanced Optimization", "order": 3},
                        ],
                    },
                ],
            },
            {
                "name": "Phase 3: Machine Learning Fundamentals",
                "description": "Core ML algorithms and techniques",
                "order": 3,
                "topics": [
                    {
                        "name": "Supervised Learning",
                        "description": "Linear/Logistic Regression, Decision Trees, SVM, Ensemble Methods",
                        "order": 1,
                        "subtopics": [
                            {"name": "Linear and Logistic Regression", "order": 1},
                            {"name": "Decision Trees and Random Forests", "order": 2},
                            {"name": "Support Vector Machines", "order": 3},
                        ],
                    },
                    {
                        "name": "Unsupervised Learning",
                        "description": "Clustering, PCA, Anomaly Detection",
                        "order": 2,
                        "subtopics": [
                            {"name": "K-Means and Hierarchical Clustering", "order": 1},
                            {"name": "Principal Component Analysis", "order": 2},
                            {"name": "Anomaly Detection Methods", "order": 3},
                        ],
                    },
                ],
            },
            {
                "name": "Phase 4: Deep Learning",
                "description": "Neural networks and deep learning architectures",
                "order": 4,
                "topics": [
                    {
                        "name": "Neural Network Basics",
                        "description": "Perceptrons, Backpropagation, Activation Functions",
                        "order": 1,
                        "subtopics": [
                            {"name": "Perceptrons and MLPs", "order": 1},
                            {"name": "Backpropagation Algorithm", "order": 2},
                            {"name": "Activation Functions", "order": 3},
                        ],
                    },
                    {
                        "name": "CNN & Computer Vision",
                        "description": "Convolutional Networks, Image Processing",
                        "order": 2,
                        "subtopics": [
                            {"name": "Convolutional Layers", "order": 1},
                            {"name": "Image Classification", "order": 2},
                            {"name": "Object Detection", "order": 3},
                        ],
                    },
                    {
                        "name": "RNN & NLP",
                        "description": "Recurrent Networks, Transformers, LLMs",
                        "order": 3,
                        "subtopics": [
                            {"name": "RNN and LSTM", "order": 1},
                            {"name": "Transformers", "order": 2},
                            {"name": "Large Language Models", "order": 3},
                        ],
                    },
                ],
            },
            {
                "name": "Phase 5: ML Engineering",
                "description": "Production ML systems and MLOps",
                "order": 5,
                "topics": [
                    {
                        "name": "Model Training & Optimization",
                        "description": "Hyperparameter Tuning, Regularization, Training at Scale",
                        "order": 1,
                        "subtopics": [
                            {"name": "Hyperparameter Optimization", "order": 1},
                            {"name": "Regularization Techniques", "order": 2},
                            {"name": "Distributed Training", "order": 3},
                        ],
                    },
                    {
                        "name": "MLOps & Deployment",
                        "description": "CI/CD for ML, Model Serving, Monitoring",
                        "order": 2,
                        "subtopics": [
                            {"name": "Model Deployment Strategies", "order": 1},
                            {"name": "Model Monitoring", "order": 2},
                            {"name": "A/B Testing", "order": 3},
                        ],
                    },
                ],
            },
            {
                "name": "Phase 6: AI System Architecture",
                "description": "Designing scalable AI systems",
                "order": 6,
                "topics": [
                    {
                        "name": "Distributed Systems for AI",
                        "description": "Distributed Computing, MapReduce, Spark",
                        "order": 1,
                        "subtopics": [
                            {"name": "Distributed Computing Basics", "order": 1},
                            {"name": "Apache Spark for ML", "order": 2},
                            {"name": "Data Parallelism", "order": 3},
                        ],
                    },
                    {
                        "name": "Real-time AI Systems",
                        "description": "Stream Processing, Low-latency Inference",
                        "order": 2,
                        "subtopics": [
                            {"name": "Stream Processing", "order": 1},
                            {"name": "Low-latency Serving", "order": 2},
                            {"name": "Edge AI", "order": 3},
                        ],
                    },
                ],
            },
            {
                "name": "Phase 7: Data Engineering for AI",
                "description": "Building robust data pipelines",
                "order": 7,
                "topics": [
                    {
                        "name": "Data Pipeline Design",
                        "description": "ETL, Data Lakes, Feature Stores",
                        "order": 1,
                        "subtopics": [
                            {"name": "ETL Processes", "order": 1},
                            {"name": "Data Lakes and Warehouses", "order": 2},
                            {"name": "Feature Stores", "order": 3},
                        ],
                    },
                    {
                        "name": "Data Quality & Governance",
                        "description": "Data Validation, Privacy, Compliance",
                        "order": 2,
                        "subtopics": [
                            {"name": "Data Validation", "order": 1},
                            {"name": "Data Privacy", "order": 2},
                            {"name": "Data Governance", "order": 3},
                        ],
                    },
                ],
            },
            {
                "name": "Phase 8: Advanced AI Topics",
                "description": "Cutting-edge AI research and applications",
                "order": 8,
                "topics": [
                    {
                        "name": "Reinforcement Learning",
                        "description": "Q-Learning, Policy Gradients, Deep RL",
                        "order": 1,
                        "subtopics": [
                            {"name": "Q-Learning and DQN", "order": 1},
                            {"name": "Policy Gradients", "order": 2},
                            {"name": "Actor-Critic Methods", "order": 3},
                        ],
                    },
                    {
                        "name": "Generative AI",
                        "description": "GANs, VAEs, Diffusion Models",
                        "order": 2,
                        "subtopics": [
                            {"name": "Generative Adversarial Networks", "order": 1},
                            {"name": "Variational Autoencoders", "order": 2},
                            {"name": "Diffusion Models", "order": 3},
                        ],
                    },
                ],
            },
            {
                "name": "Phase 9: AI Ethics & Safety",
                "description": "Responsible AI development",
                "order": 9,
                "topics": [
                    {
                        "name": "Fairness & Bias",
                        "description": "Bias Detection, Fair ML, Interpretability",
                        "order": 1,
                        "subtopics": [
                            {"name": "Bias Detection and Mitigation", "order": 1},
                            {"name": "Fair Machine Learning", "order": 2},
                            {"name": "Model Interpretability", "order": 3},
                        ],
                    },
                    {
                        "name": "AI Safety & Alignment",
                        "description": "Robustness, Safety, Value Alignment",
                        "order": 2,
                        "subtopics": [
                            {"name": "Adversarial Robustness", "order": 1},
                            {"name": "AI Safety Research", "order": 2},
                            {"name": "Value Alignment", "order": 3},
                        ],
                    },
                ],
            },
            {
                "name": "Phase 10: AI Leadership & Strategy",
                "description": "Leading AI teams and initiatives",
                "order": 10,
                "topics": [
                    {
                        "name": "AI Product Management",
                        "description": "AI Product Strategy, Roadmapping, Metrics",
                        "order": 1,
                        "subtopics": [
                            {"name": "AI Product Strategy", "order": 1},
                            {"name": "Success Metrics", "order": 2},
                            {"name": "Stakeholder Management", "order": 3},
                        ],
                    },
                    {
                        "name": "Building AI Teams",
                        "description": "Team Structure, Hiring, Culture",
                        "order": 2,
                        "subtopics": [
                            {"name": "AI Team Structure", "order": 1},
                            {"name": "Hiring Best Practices", "order": 2},
                            {"name": "AI Culture", "order": 3},
                        ],
                    },
                ],
            },
        ]

        # Insert phases, topics, and subtopics
        for phase_data in phases_data:
            topics_data = phase_data.pop("topics", [])
            phase = Phase(**phase_data)
            db.add(phase)
            db.flush()

            for topic_data in topics_data:
                subtopics_data = topic_data.pop("subtopics", [])
                topic_data["phase_id"] = phase.id
                topic = Topic(**topic_data)
                db.add(topic)
                db.flush()

                for subtopic_data in subtopics_data:
                    subtopic_data["topic_id"] = topic.id
                    subtopic = Subtopic(**subtopic_data)
                    db.add(subtopic)
                    db.flush()

                    # Add mastery components for each subtopic
                    mastery_types = ["Theory", "Practice", "Project"]
                    for idx, comp_type in enumerate(mastery_types):
                        component = MasteryComponent(
                            subtopic_id=subtopic.id,
                            name=f"{comp_type} - {subtopic.name}",
                            description=f"{comp_type} component for mastering {subtopic.name}",
                            component_type=comp_type.lower(),
                        )
                        db.add(component)

        # Create achievements
        achievements_data = [
            {
                "name": "First Step",
                "description": "Complete your first subtopic",
                "icon": "🎯",
                "points": 10,
                "requirement": "Complete 1 subtopic",
            },
            {
                "name": "Getting Started",
                "description": "Complete 5 subtopics",
                "icon": "🚀",
                "points": 50,
                "requirement": "Complete 5 subtopics",
            },
            {
                "name": "Phase Master",
                "description": "Complete an entire phase",
                "icon": "🏆",
                "points": 100,
                "requirement": "Complete 1 full phase",
            },
            {
                "name": "Dedicated Learner",
                "description": "Study for 10 hours",
                "icon": "📚",
                "points": 50,
                "requirement": "Log 10 hours of study time",
            },
            {
                "name": "Marathon Learner",
                "description": "Study for 100 hours",
                "icon": "🎓",
                "points": 200,
                "requirement": "Log 100 hours of study time",
            },
            {
                "name": "Streak Master",
                "description": "Maintain a 7-day streak",
                "icon": "🔥",
                "points": 75,
                "requirement": "Study for 7 consecutive days",
            },
        ]

        for achievement_data in achievements_data:
            achievement = Achievement(**achievement_data)
            db.add(achievement)

        # Create initial stats
        stats = Stats()
        db.add(stats)

        db.commit()
        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
