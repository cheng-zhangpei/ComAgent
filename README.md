# Intelligent Agent Framework for Complex Task Management

## Overview

This project aims to develop an intelligent agent framework capable of managing and executing complex tasks in distributed environments, such as Kubernetes (K8s) clusters. The framework is designed to provide a flexible, scalable, and efficient solution for intelligent operations, focusing on task decomposition, dynamic tool invocation, and efficient resource management.

### Key Features

- **Expert and Sub-Task Agents**: The framework defines `Expert Agents` responsible for high-level task planning and `Sub-Task Agents` for executing individual components of a task.
- **DAG-Based Task Scheduling**: Tasks are dynamically decomposed and scheduled based on Directed Acyclic Graphs (DAGs), ensuring proper execution order and dependency management.
- **Semaphore Synchronization**: A semaphore-based synchronization mechanism ensures that tasks are executed in the correct sequence, avoiding conflicts and ensuring efficient resource usage.
- **Message Queue Communication**: The framework uses RabbitMQ for inter-agent communication, enabling reliable message passing and event-driven processing.
- **Etcd-Based Caching**: Agents utilize Etcd for both local and global caching, allowing efficient data sharing and state management across the system.

## Architecture

### Components

1. **Expert Agent**: 
   - Responsible for the overall planning and decomposition of complex tasks.
   - Uses DAG to structure tasks and coordinates with `Sub-Task Agents` for execution.
   - Sends and receives messages via RabbitMQ to communicate with other agents.

2. **Sub-Task Agent**:
   - Executes specific subtasks as directed by the `Expert Agent`.
   - Manages dependencies using a semaphore synchronization mechanism.
   - Communicates task progress and results back to the `Expert Agent` and `Job Supervisor`.

3. **Job Scheduler**:
   - Schedules and monitors tasks based on the DAG generated by the `Expert Agent`.
   - Dynamically assigns tasks to `Sub-Task Agents` and ensures proper execution order.

4. **Job Supervisor**:
   - Monitors the execution status of tasks using a bitmap.
   - Ensures all tasks are completed before aggregating results and reporting back to the `Expert Agent`.

5. **Message Queue (RabbitMQ)**:
   - Facilitates communication between agents.
   - Supports multi-level queues and message prioritization to optimize task execution.

6. **Caching (Etcd)**:
   - **Local Cache**: Each agent maintains its own local cache in Etcd for storing temporary data.
   - **Global Cache**: Shared across agents for storing common data, enabling efficient state sharing and reducing redundancy.

### Communication Flow

1. **Task Initialization**:
   - The `Expert Agent` initiates a high-level task and decomposes it into subtasks.
   - The subtasks are structured into a DAG and distributed to `Sub-Task Agents`.

2. **Task Execution**:
   - `Sub-Task Agents` execute their assigned tasks, using the semaphore mechanism to manage dependencies.
   - Each `Sub-Task Agent` communicates progress and results via RabbitMQ to the `Job Supervisor`.

3. **Result Aggregation**:
   - The `Job Supervisor` collects and verifies the completion of all subtasks.
   - Once all subtasks are completed, results are aggregated and sent back to the `Expert Agent`.

4. **Caching**:
   - Throughout task execution, agents interact with Etcd to store and retrieve data from their local and global caches.
   - The caching mechanism ensures that relevant data is readily available, reducing the need for redundant computation.

## Getting Started

### Prerequisites

- **Python 3.x**
- **RabbitMQ**: Make sure RabbitMQ is installed and running on your system.
- **Etcd**: Ensure that Etcd is installed and configured.
- **Python Libraries**:
  - `pika` (for RabbitMQ communication)
  - `etcd` (for Etcd interaction)
  - `threading` (for multi-threaded operations)

### Installation