
admin_defaults = {
    'email': 'admin@user.com',
    'is_superuser': True,
    'is_staff': True
}
moderator_defaults = {
    'email': 'mod@user.com',
    'is_superuser': False,
    'is_staff': True
}
user_defaults = {
    'email': 'regular@user.com',
    'is_superuser': False,
    'is_staff': False
}

tags_list = [
    'Python', 'C++', 'JavaScript', 'React', 'Node',
    'SQL', 'Django', 'MongoDB', 'HTML', 'CSS', 'Computer Science'
]

article_tags = [
    ['Django', 'Python', 'SQL'], 
    ['JavaScript', 'HTML', 'CSS'], 
    ['MongoDB', 'Node', 'React'], 
    ['Computer Science', 'C++']
]

status_list = ['draft', 'publish', 'archived', 'publish']


article_data = [
    {
        "title": "Mastering Django QuerySets: Tips for Cleaner Code",
        "content": """
Django's ORM is one of its most powerful features, allowing developers to interact with databases using clean, expressive Python code. Yet, many developers underuse it, sticking to basic filter and get calls. In this article, we’ll explore how to leverage QuerySets more effectively to write cleaner, faster, and more maintainable code.

What is a QuerySet?

A QuerySet represents a collection of database rows mapped to Django model instances. They're lazy, meaning the database is only hit when needed, and they support powerful chaining of filters, annotations, and expressions.

select_related and prefetch_related

When dealing with related models, using select_related and prefetch_related can drastically reduce the number of queries. For example, accessing the author of each post in a list can be done with just one query using select_related.

annotate for counts and aggregates

If you need to count related objects, like the number of comments on each blog post, annotate is the tool for the job. Combined with aggregate functions, it can give you insights directly in the query without looping through data manually.

Chaining filters

Django lets you chain multiple filters for readable, modular query building. This is especially useful when dealing with complex search or filtering logic in views.

Real-World Application

Imagine a blog view that displays posts with their author and number of comments. Without optimization, this could easily result in dozens of queries. With select_related for authors, annotate for comment counts, and careful filtering, you can reduce this to just two or three queries — much faster and more efficient.

Conclusion

Mastering Django QuerySets is about more than writing code that works — it's about writing code that scales. By using Django's ORM tools well, your apps will run faster, your code will be cleaner, and your development will be a whole lot smoother.

""",
        "tags": ['Python', 'Django', 'SQL']
    },
    {
        "title": "Why React Still Dominates Front-End Development in 2025",
        "content": """
Despite the rise of new frameworks like Svelte and SolidJS, React continues to be the go-to for 
production-ready front-end applications in 2025.

**React’s Continued Popularity:**
- Ecosystem stability
- Declarative component model
- New features like Server Components and Suspense

React isn’t just surviving — it’s thriving.
""",
        "tags": ['JavaScript', 'React', 'HTML', 'CSS']
    },
    {
        "title": "Intro to SQL Joins: From Basics to Advanced Patterns",
        "content": """
SQL is the language of relational databases, and understanding joins is essential for working with related data across tables. Joins allow you to fetch combined data from multiple tables in a single query, which is crucial for performance and accuracy.

What is a SQL Join?

A join combines rows from two or more tables based on a related column. This is how relational databases bring together normalized data into meaningful relationships.

Types of Joins

INNER JOIN returns records that have matching values in both tables. It's the most common type and is used when you only want records that have a relationship in both tables.

LEFT JOIN returns all records from the left table and the matched records from the right. If there’s no match, you still get the left table’s data, with nulls from the right.

RIGHT JOIN does the reverse of LEFT JOIN, giving you all records from the right and any matches from the left.

FULL OUTER JOIN combines all records from both tables, filling in nulls where there are no matches. Note that not all SQL engines support this directly.

Practical Use Cases

In a user-order system, joining users and orders lets you create detailed reports, such as users with or without orders, order counts per user, or revenue breakdowns. It’s also essential for dashboards, analytics, and data exports.

Advanced Joins

You can also join on calculated fields, use subqueries in joins, and apply multi-table joins for complex reporting needs. Common Table Expressions, or CTEs, help make these readable and reusable.

Conclusion

Understanding SQL joins is a foundational skill for any backend, data, or full-stack developer. Mastering them means writing fewer, faster,

""",
        "tags": ['SQL', 'Python', 'Computer Science']
    },
    {
        "title": "CSS Grid vs Flexbox: When and Why to Use Each",
        "content": """
CSS Grid and Flexbox are both powerful layout systems, but they shine in different scenarios.

**Quick rules of thumb:**
- Use **Flexbox** for one-dimensional layouts (row OR column).
- Use **Grid** for two-dimensional layouts (row AND column).

Learning to combine both is the key to modern responsive design.
""",
        "tags": ['CSS', 'HTML', 'JavaScript']
    }
]
