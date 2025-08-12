import json
import os
import streamlit as st
from datetime import datetime, timedelta

PLANS_FILE = "plans.json"

def load_plans():
    if os.path.exists(PLANS_FILE):
        with open(PLANS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return [] # Dosya boş veya bozuksa
    return []

def save_plans(plans):
    with open(PLANS_FILE, 'w', encoding='utf-8') as f:
        json.dump(plans, f, ensure_ascii=False, indent=4)

def create_new_plan(goal, weekly_tasks, learning_style, motivation_message, survey_answers=None):
    """
    Yeni bir plan oluşturur
    """
    plan = {
        "id": str(datetime.now().timestamp()),
        "goal": goal,
        "learning_style": learning_style,
        "motivation_message": motivation_message,
        "created_date": datetime.now().isoformat(),
        "weekly_tasks": weekly_tasks,
        "current_week": 1,
        "completed_tasks": [],
        "weekly_progress": [],
        "survey_answers": survey_answers or []
    }
    return plan

def get_current_week_tasks(plan):
    """
    Mevcut haftanın görevlerini döndürür
    """
    if not plan.get('weekly_tasks'):
        return []
    
    current_week = plan.get('current_week', 1)
    week_index = (current_week - 1) % len(plan['weekly_tasks'])
    return plan['weekly_tasks'][week_index]

def mark_task_completed(plan_id, day, task_index):
    """
    Bir görevi tamamlandı olarak işaretler
    """
    plans = load_plans()
    for plan in plans:
        if plan['id'] == plan_id:
            completed_task = {
                "day": day,
                "task_index": task_index,
                "completed_date": datetime.now().isoformat()
            }
            if 'completed_tasks' not in plan:
                plan['completed_tasks'] = []
            plan['completed_tasks'].append(completed_task)
            save_plans(plans)
            return True
    return False

def unmark_task_completed(plan_id, day, task_index):
    """
    Bir görevin tamamlandı işaretini kaldırır
    """
    plans = load_plans()
    for plan in plans:
        if plan['id'] == plan_id:
            if 'completed_tasks' in plan:
                # Bu görevi completed_tasks listesinden kaldır
                plan['completed_tasks'] = [
                    task for task in plan['completed_tasks']
                    if not (task.get('day') == day and task.get('task_index') == task_index)
                ]
                save_plans(plans)
                return True
    return False

def calculate_weekly_progress(plan):
    """
    Haftalık ilerleme yüzdesini hesaplar - Tüm haftanın görevlerine göre hesaplar
    """
    if not plan.get('weekly_tasks'):
        return 0
    
    total_tasks = 0
    completed_tasks = 0
    
    # Tüm haftanın görevlerini döngüye al
    for week_tasks in plan['weekly_tasks']:
        if not isinstance(week_tasks, dict) or 'tasks' not in week_tasks:
            continue
            
        day_tasks = week_tasks.get('tasks', [])
        total_tasks += len(day_tasks)
        
        # Bu günün tamamlanan görevlerini say
        for task_index, task in enumerate(day_tasks):
            for completed_task in plan.get('completed_tasks', []):
                if (completed_task.get('day') == week_tasks.get('day') and 
                    completed_task.get('task_index') == task_index):
                    completed_tasks += 1
                    break
    
    return (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

def get_weekly_stats(plan):
    """
    Haftalık istatistikleri döndürür - Tüm haftanın görevlerine göre hesaplar
    """
    if not plan.get('weekly_tasks'):
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "progress_percentage": 0
        }
    
    total_tasks = 0
    completed_tasks = 0
    
    # Tüm haftanın görevlerini döngüye al
    for week_tasks in plan['weekly_tasks']:
        if not isinstance(week_tasks, dict) or 'tasks' not in week_tasks:
            continue
            
        day_tasks = week_tasks.get('tasks', [])
        total_tasks += len(day_tasks)
        
        # Bu günün tamamlanan görevlerini say
        for task_index, task in enumerate(day_tasks):
            for completed_task in plan.get('completed_tasks', []):
                if (completed_task.get('day') == week_tasks.get('day') and 
                    completed_task.get('task_index') == task_index):
                    completed_tasks += 1
                    break
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "progress_percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    }