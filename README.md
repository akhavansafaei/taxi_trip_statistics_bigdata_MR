# Taxi Trip Statistics - Big Data MapReduce

A collection of Hadoop MapReduce implementations for clustering taxi trip pickup locations using various clustering algorithms. This project demonstrates different approaches to analyzing taxi trip data using distributed computing with Hadoop Streaming.

## Overview

This repository contains multiple implementations of clustering algorithms applied to taxi trip data:
- **K-Means Clustering** (Root directory)
- **PAM (Partitioning Around Medoids)** with different medoid calculation strategies (1, 1st, 2nd, 3rd directories)

The clustering is performed on taxi pickup location coordinates (x, y) extracted from trip data.

## Data Format

### Taxis.txt
Format: `taxi_id,field1,field2,year`
```
470,0,80,2018
332,11,88,2013
254,10,62,2018
```

### Trips.txt
Format: `trip_id,taxi_id,cost,duration,pickup_x,pickup_y,dropoff_x,dropoff_y`
```
0,470,117.32,64.27,54.736,91.185,20.488,93.348
1,332,92.25,49.76,25.684,14.951,3.572,49.541
2,254,82.34,48.56,54.736,91.185,33.385,73.821
```

## Implementations

### Root Directory: K-Means Clustering
Uses centroid-based clustering with mean calculations.

**Files:**
- `mapper.py` - Assigns points to nearest centroid
- `reducer.py` - Calculates new centroids as mean of cluster points
- `reader.py` - Checks convergence between iterations
- `printer.py` - Visualizes clustering results
- `task2-run.sh` - Execution script

**Algorithm:**
1. Initialize centroids from `centroids.txt`
2. Assign each point to nearest centroid (Euclidean distance)
3. Calculate new centroids as mean of assigned points
4. Repeat until convergence (distance < 1)

### 1st Directory: PAM with Mean
Implements Partitioning Around Medoids using mean for medoid calculation.

**Files:**
- `mapper.py` - Assigns points to nearest medoid
- `reducer.py` - Calculates new medoids using mean
- `task2-run.sh` - Execution script

**Features:**
- Random initial medoid selection on first iteration
- Uses mean of cluster points for new medoids
- Iterative refinement with configurable iterations

### 2nd Directory: PAM with Mode
Similar to 1st directory but uses statistical mode for medoid calculation.

**Files:**
- `pam_mapper.py` - Assigns points to nearest medoid
- `pam_reducer.py` - Calculates new medoids using mode
- `task2-run.sh` - Execution script

**Approach:**
- Mode-based medoid calculation for more robust clustering
- Better handling of outliers compared to mean-based approach

### 3rd Directory: PAM with Convergence Checking
Advanced PAM implementation with built-in convergence detection.

**Files:**
- `pam_mapper.py` - Assigns points to nearest medoid
- `pam_reducer.py` - Calculates true medoids (point with minimum total distance)
- `task2-run.sh` - Execution script

**Features:**
- True medoid calculation (point minimizing total intra-cluster distance)
- Convergence threshold checking
- Automatic termination when clusters stabilize

### 1 Directory: PAM Variant
Another PAM implementation with mixed approach.

**Files:**
- `mapper.py` - Combines random initialization and file-based medoids
- `reducer.py` - Uses mode for medoid calculation
- `task2-run.sh` - Execution script
- `readme.txt` - Basic usage instructions

## Prerequisites

- Hadoop 3.1.4 or compatible version
- Python 3.x
- Required Python packages:
  - `matplotlib` (for visualization)
  - `scipy` (for distance calculations)
  - `statistics` (built-in)

## Usage

### Basic Execution

1. Make the execution script executable:
```bash
chmod +x task2-run.sh
```

2. Run the clustering algorithm:
```bash
./task2-run.sh <K> <V>
```
- `K`: Number of clusters
- `V`: Maximum number of iterations

Example:
```bash
./task2-run.sh 3 10
```

### Hadoop Command Structure

The scripts use Hadoop Streaming with the following pattern:

```bash
hadoop jar ./hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=1 \
    -file ./mapper.py \
    -mapper "./mapper.py $i $K" \
    -file ./reducer.py \
    -reducer ./reducer.py \
    -input /Trips.txt \
    -output /mapreduce-output$i
```

### Input Data Setup

1. Upload data to HDFS:
```bash
hadoop fs -put Taxis.txt /input/
hadoop fs -put Trips.txt /input/
```

2. Ensure initial centroids/medoids file exists locally (for applicable implementations)

### Output

The clustering results are stored in HDFS at `/output/` or `/mapreduce-output$i` depending on the implementation. Each iteration produces:
- Cluster assignments
- Updated centroid/medoid coordinates
- Convergence status (in some implementations)

## Algorithm Comparison

| Implementation | Initialization | Medoid Calculation | Convergence Check | Best For |
|---------------|---------------|-------------------|-------------------|----------|
| Root (K-Means) | File-based centroids | Mean | Manual | Standard clustering |
| 1st (PAM-Mean) | Random | Mean | Manual | Quick clustering |
| 2nd (PAM-Mode) | Random | Mode | Manual | Outlier-resistant |
| 3rd (PAM-True) | Random | True medoid | Automatic | Accurate clustering |
| 1 (PAM-Mixed) | Random/File | Mode | Manual | Flexible approach |

## Visualization

Use `printer.py` (root directory) to visualize clustering results:

```bash
python printer.py
```

This generates a scatter plot showing:
- Cluster 0: Red points
- Cluster 1: Green points
- Cluster 2: Blue points
- Centroids/Medoids: Yellow points

## Project Structure

```
.
├── README.md
├── mapper.py           # K-means mapper
├── reducer.py          # K-means reducer
├── reader.py           # Convergence checker
├── printer.py          # Visualization tool
├── task2-run.sh        # K-means execution script
├── 1/                  # PAM mixed variant
├── 1st/                # PAM with mean
├── 2nd/                # PAM with mode
└── 3rd/                # PAM with convergence
```

## Key Concepts

### MapReduce Flow

**Map Phase:**
- Read trip data from STDIN
- Extract pickup coordinates (fields 4 and 5)
- Calculate distance to each centroid/medoid
- Emit: `cluster_id \t x \t y`

**Reduce Phase:**
- Group points by cluster_id
- Calculate new centroid/medoid
- Output updated cluster centers

### Distance Metric

All implementations use Euclidean distance:
```python
distance = sqrt((x1 - x2)² + (y1 - y2)²)
```

### Convergence Criteria

- **K-Means (root):** Centroid movement < 1 in both dimensions
- **PAM variants:** Configurable via iterations or automatic threshold checking

## Troubleshooting

1. **Permission denied:** Run `chmod +x task2-run.sh`
2. **Hadoop not found:** Ensure Hadoop is installed and in PATH
3. **Output directory exists:** Remove old output before running
   ```bash
   hadoop fs -rm -r /output/
   ```
4. **Python not found:** Ensure Python 3.x is installed

## Performance Considerations

- Use appropriate number of reduce tasks based on cluster size
- For large datasets, increase Hadoop memory settings
- Random initialization may produce different results across runs
- More iterations generally improve clustering quality but increase runtime

## License

This project is for educational purposes demonstrating big data clustering techniques with Hadoop MapReduce.

## Contributing

This repository contains different experimental approaches to taxi trip clustering. Each directory represents a different strategy and can be modified independently.
